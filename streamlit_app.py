"""
Streamlit app for Sustainable Real Estate Calculator
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
from sustainable_calculator import (
    SustainableRealEstateCalculator,
    Asset,
    SCI,
    Participation,
    PEFundParticipation
)

def main():
    """Main function for the Streamlit app."""
    st.set_page_config(page_title="Sustainable Real Estate Calculator", page_icon="🏢", layout="wide")
    
    st.title("Sustainable Real Estate Investment Calculator")
    st.markdown("""
    This tool calculates sustainable investment percentages for real estate portfolios according to 
    EU Taxonomy, SFDR, and industry guidelines from ASPIM and AMF.
    """)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    pages = ["Dashboard", "Fund Information", "Direct Assets", "SCIs", 
             "Controlled Participations", "Uncontrolled Participations", 
             "Minority Stakes", "PE Fund Participations"]
    page = st.sidebar.radio("Go to", pages)
    
    # Initialize session state
    if 'calculator' not in st.session_state:
        st.session_state.calculator = SustainableRealEstateCalculator(
            fund_name="",
            fund_type="",
            reporting_date=""
        )
        
    if 'direct_assets' not in st.session_state:
        st.session_state.direct_assets = []
        
    if 'scis' not in st.session_state:
        st.session_state.scis = []
        
    if 'controlled_participations' not in st.session_state:
        st.session_state.controlled_participations = []
        
    if 'uncontrolled_participations' not in st.session_state:
        st.session_state.uncontrolled_participations = []
        
    if 'minority_stakes' not in st.session_state:
        st.session_state.minority_stakes = []
        
    if 'pe_fund_participations' not in st.session_state:
        st.session_state.pe_fund_participations = []
    
    # Display appropriate page based on selection
    if page == "Dashboard":
        display_dashboard()
    elif page == "Fund Information":
        display_fund_information()
    elif page == "Direct Assets":
        display_direct_assets()
    elif page == "SCIs":
        display_scis()
    elif page == "Controlled Participations":
        display_controlled_participations()
    elif page == "Uncontrolled Participations":
        display_uncontrolled_participations()
    elif page == "Minority Stakes":
        display_minority_stakes()
    elif page == "PE Fund Participations":
        display_pe_fund_participations()
    
    # Add a sample data button to the sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("Load Sample Data"):
        load_sample_data()
        st.sidebar.success("Sample data loaded successfully!")
        st.experimental_rerun()

def display_dashboard():
    """Display the main dashboard with calculation results."""
    st.header("Dashboard")
    
    if not st.session_state.calculator.fund_name:
        st.warning("Please enter fund information to start the calculation.")
        return
    
    # Recalculate results with the current data
    update_calculator()
    results = st.session_state.calculator.calculate_total()
    
    # Display fund information
    st.subheader("Fund Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Fund Name", results['fund_info']['fund_name'])
    with col2:
        st.metric("Fund Type", results['fund_info']['fund_type'])
    with col3:
        st.metric("Reporting Date", results['fund_info']['reporting_date'])
    
    # Display overall sustainability metrics
    st.subheader("Sustainability Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Value (€M)", f"{results['fund_total']['total_value']:.2f}")
    with col2:
        st.metric("Sustainable Value (€M)", f"{results['fund_total']['sustainable_value']:.2f}")
    with col3:
        st.metric("Sustainable Percentage", f"{results['fund_total']['sustainable_percentage']:.2f}%")
    
    # Display sustainability assessment
    st.subheader("Sustainability Assessment")
    sustainable_percentage = results['fund_total']['sustainable_percentage']
    
    if sustainable_percentage >= 75:
        st.success("High sustainable investment proportion (>75%)")
    elif sustainable_percentage >= 50:
        st.success("Substantial sustainable investment proportion (50-75%)")
    elif sustainable_percentage >= 20:
        st.warning("Moderate sustainable investment proportion (20-50%)")
    else:
        st.error("Limited sustainable investment proportion (<20%)")
    
    # Display regulatory classification suggestion
    st.subheader("Regulatory Classification Guidance")
    
    if sustainable_percentage >= 50:
        st.info("✅ Qualifies for Article 8 with sustainable investments")
        if sustainable_percentage >= 80:
            st.info("✅ May consider Article 9 classification (if environmental/social objective is the target)")
    elif sustainable_percentage >= 20:
        st.info("✅ Qualifies for Article 8")
    else:
        st.info("✅ Consider Article 6 classification")
    
    # Display breakdown table
    st.subheader("Investment Category Breakdown")
    
    categories = [
        ("Direct Assets", results["direct_assets"]),
        ("100% Owned SCIs", results["scis"]),
        ("Controlled Participations", results["controlled_participations"]),
        ("Uncontrolled Participations", results["uncontrolled_participations"]),
        ("Minority Stakes", results["minority_stakes"]),
        ("PE Fund Participations", results["pe_fund_participations"]),
        ("FUND TOTAL", results["fund_total"])
    ]
    
    df = pd.DataFrame({
        "Category": [c[0] for c in categories],
        "Total Value (€M)": [c[1]['total_value'] for c in categories],
        "Sustainable Value (€M)": [c[1]['sustainable_value'] for c in categories],
        "Sustainable %": [c[1]['sustainable_percentage'] for c in categories]
    })
    
    st.dataframe(df.style.format({
        "Total Value (€M)": "{:.2f}",
        "Sustainable Value (€M)": "{:.2f}",
        "Sustainable %": "{:.2f}%"
    }), use_container_width=True)
    
    # Create visualizations
    st.subheader("Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create pie chart for sustainable vs non-sustainable
        fig_pie = px.pie(
            names=["Sustainable", "Non-Sustainable"],
            values=[
                results["fund_total"]["sustainable_value"],
                results["fund_total"]["total_value"] - results["fund_total"]["sustainable_value"]
            ],
            title="Sustainable vs Non-Sustainable Investments",
            color_discrete_sequence=["#4CAF50", "#F44336"]
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Create bar chart for category comparison
        fig_bar = px.bar(
            df[:-1],  # Exclude the FUND TOTAL row
            x="Category",
            y=["Sustainable Value (€M)", "Total Value (€M)"],
            title="Sustainable Value by Category",
            barmode="overlay"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Display a download button for the report
    report_json = json.dumps(results, indent=2)
    st.download_button(
        label="Download Report (JSON)",
        data=report_json,
        file_name="sustainable_real_estate_report.json",
        mime="application/json"
    )

def display_fund_information():
    """Display and edit fund information."""
    st.header("Fund Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fund_name = st.text_input(
            "Fund Name", 
            value=st.session_state.calculator.fund_name if st.session_state.calculator.fund_name else ""
        )
    
    with col2:
        fund_type = st.selectbox(
            "Fund Type", 
            ["", "Article 6", "Article 8", "Article 9"],
            index=0 if not st.session_state.calculator.fund_type else 
                  ["", "Article 6", "Article 8", "Article 9"].index(st.session_state.calculator.fund_type)
        )
    
    with col3:
        reporting_date = st.date_input(
            "Reporting Date",
            value=None
        )
        reporting_date = reporting_date.strftime("%Y-%m-%d") if reporting_date else ""
    
    if st.button("Save Fund Information"):
        st.session_state.calculator.fund_name = fund_name
        st.session_state.calculator.fund_type = fund_type
        st.session_state.calculator.reporting_date = reporting_date
        st.success("Fund information saved successfully!")
    
    # Sustainability criteria thresholds
    st.subheader("Sustainability Criteria Thresholds")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_sdg_score = st.number_input(
            "Minimum UN SDG Score (0-10)",
            min_value=0.0,
            max_value=10.0,
            value=st.session_state.calculator.min_sdg_score,
            step=0.1
        )
    
    with col2:
        min_esg_score = st.number_input(
            "Minimum ESG Score (0-20)",
            min_value=0.0,
            max_value=20.0,
            value=st.session_state.calculator.min_esg_score,
            step=0.1
        )
    
    with col3:
        min_msci_score = st.number_input(
            "Minimum MSCI Score (0-10)",
            min_value=0.0,
            max_value=10.0,
            value=st.session_state.calculator.min_msci_score,
            step=0.1
        )
    
    if st.button("Save Thresholds"):
        st.session_state.calculator.min_sdg_score = min_sdg_score
        st.session_state.calculator.min_esg_score = min_esg_score
        st.session_state.calculator.min_msci_score = min_msci_score
        st.success("Threshold values saved successfully!")

def display_direct_assets():
    """Display and edit direct assets."""
    st.header("Direct Assets")
    
    # Initialize asset_to_edit
    asset_to_edit = 0
    
    # Display existing assets in a table
    if st.session_state.direct_assets:
        st.subheader("Existing Assets")
        assets_data = []
        
        for i, asset in enumerate(st.session_state.direct_assets):
            is_sustainable = asset.is_sustainable(
                st.session_state.calculator.min_sdg_score,
                st.session_state.calculator.min_esg_score,
                st.session_state.calculator.min_msci_score
            )
            
            assets_data.append({
                "ID": asset.asset_id,
                "Name": asset.name,
                "Value (€M)": asset.market_value,
                "EPC": asset.epc_rating or "-",
                "Top 15%": "Yes" if asset.top_15_percent else "No",
                "NZEB": "Yes" if asset.nzeb_compliant else "No",
                "SDG Score": asset.un_sdg_score or "-",
                "ESG Score": asset.esg_score or "-",
                "DNSH": "Yes" if asset.dnsh_compliant else "No",
                "Sustainable": "Yes" if is_sustainable else "No",
                "Actions": i
            })
        
        df = pd.DataFrame(assets_data)
        st.dataframe(df.drop(columns=["Actions"]), use_container_width=True)
        
        # Action buttons for each asset
        col1, col2 = st.columns(2)
        with col1:
            asset_to_edit = st.number_input(
                "Select asset to edit (row number)",
                min_value=0,
                max_value=len(st.session_state.direct_assets)-1 if st.session_state.direct_assets else 0,
                value=0
            )
        with col2:
            if st.button("Delete Selected Asset") and st.session_state.direct_assets:
                st.session_state.direct_assets.pop(asset_to_edit)
                st.success("Asset deleted successfully!")
                st.experimental_rerun()
    
    # Form to add or edit an asset
    st.subheader("Add New Asset" if not st.session_state.direct_assets else "Edit Asset")
    
    asset_to_add = Asset(
        asset_id="",
        name="",
        market_value=0.0
    )
    
    # If editing, pre-fill the form with the selected asset's values
    if st.session_state.direct_assets and len(st.session_state.direct_assets) > 0:
        asset_to_add = st.session_state.direct_assets[asset_to_edit]
    
    col1, col2 = st.columns(2)
    
    with col1:
        asset_id = st.text_input("Asset ID", value=asset_to_add.asset_id)
        asset_name = st.text_input("Asset Name", value=asset_to_add.name)
        market_value = st.number_input("Market Value (€M)", value=asset_to_add.market_value, step=0.1)
        epc_rating = st.selectbox(
            "EPC Rating",
            ["", "A", "B", "C", "D", "E", "F", "G"],
            index=0 if not asset_to_add.epc_rating else ["", "A", "B", "C", "D", "E", "F", "G"].index(asset_to_add.epc_rating)
        )
        top_15_percent = st.checkbox("In Top 15% of Building Stock", value=asset_to_add.top_15_percent)
    
    with col2:
        nzeb_compliant = st.checkbox("NZEB -10% Compliant", value=asset_to_add.nzeb_compliant)
        un_sdg_score = st.slider(
            "UN SDG Score (0-10)",
            min_value=0.0,
            max_value=10.0,
            value=asset_to_add.un_sdg_score if asset_to_add.un_sdg_score is not None else 0.0,
            step=0.1
        )
        esg_score = st.slider(
            "ESG Score (0-20)",
            min_value=0.0,
            max_value=20.0,
            value=asset_to_add.esg_score if asset_to_add.esg_score is not None else 0.0,
            step=0.1
        )
        msci_score = st.slider(
            "MSCI Score (0-10)",
            min_value=0.0,
            max_value=10.0,
            value=asset_to_add.msci_score if asset_to_add.msci_score is not None else 0.0,
            step=0.1
        )
        dnsh_compliant = st.checkbox("DNSH Compliant", value=asset_to_add.dnsh_compliant)
    
    st.subheader("Renovation Information (if applicable)")
    col1, col2 = st.columns(2)
    
    with col1:
        renovation_energy = st.number_input(
            "Renovation Energy Reduction (%)",
            min_value=0.0,
            max_value=100.0,
            value=asset_to_add.renovation_energy_reduction if asset_to_add.renovation_energy_reduction is not None else 0.0,
            step=0.1
        )
    
    with col2:
        renovation_ghg = st.number_input(
            "Renovation GHG Reduction (%)",
            min_value=0.0,
            max_value=100.0,
            value=asset_to_add.renovation_ghg_reduction if asset_to_add.renovation_ghg_reduction is not None else 0.0,
            step=0.1
        )
    
    if st.button("Save Asset"):
        new_asset = Asset(
            asset_id=asset_id,
            name=asset_name,
            market_value=market_value,
            epc_rating=epc_rating if epc_rating else None,
            top_15_percent=top_15_percent,
            nzeb_compliant=nzeb_compliant,
            renovation_energy_reduction=renovation_energy if renovation_energy > 0 else None,
            renovation_ghg_reduction=renovation_ghg if renovation_ghg > 0 else None,
            un_sdg_score=un_sdg_score if un_sdg_score > 0 else None,
            esg_score=esg_score if esg_score > 0 else None,
            msci_score=msci_score if msci_score > 0 else None,
            dnsh_compliant=dnsh_compliant
        )
        
        if st.session_state.direct_assets:
            # Update existing asset
            st.session_state.direct_assets[asset_to_edit] = new_asset
            st.success("Asset updated successfully!")
        else:
            # Add new asset
            st.session_state.direct_assets.append(new_asset)
            st.success("Asset added successfully!")
        
        update_calculator()
        st.experimental_rerun()

def display_scis():
    """Display and manage SCIs (100% owned)."""
    st.header("SCIs (100% Owned)")
    
    # Display existing SCIs
    if st.session_state.scis:
        st.subheader("Existing SCIs")
        
        scis_data = []
        for i, sci in enumerate(st.session_state.scis):
            sustainable_value = sci.sustainable_value(
                st.session_state.calculator.min_sdg_score,
                st.session_state.calculator.min_esg_score,
                st.session_state.calculator.min_msci_score
            )
            sustainable_percentage = 0
            if sci.total_value() > 0:
                sustainable_percentage = 100.0 * sustainable_value / sci.total_value()
                
            scis_data.append({
                "ID": sci.sci_id,
                "Name": sci.name,
                "Total Value (€M)": sci.total_value(),
                "Sustainable Value (€M)": sustainable_value,
                "Sustainable %": f"{sustainable_percentage:.2f}%",
                "Number of Assets": len(sci.assets),
                "Actions": i
            })
        
        df = pd.DataFrame(scis_data)
        st.dataframe(df.drop(columns=["Actions"]), use_container_width=True)
        
        # SCI selection for viewing/editing
        sci_to_view = st.selectbox(
            "Select SCI to view/edit",
            range(len(st.session_state.scis)),
            format_func=lambda i: st.session_state.scis[i].name
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Delete Selected SCI"):
                st.session_state.scis.pop(sci_to_view)
                st.success("SCI deleted successfully!")
                update_calculator()
                st.experimental_rerun()
        
        # Display selected SCI details
        sci = st.session_state.scis[sci_to_view]
        st.subheader(f"Assets in {sci.name}")
        
        if sci.assets:
            assets_data = []
            for i, asset in enumerate(sci.assets):
                is_sustainable = asset.is_sustainable(
                    st.session_state.calculator.min_sdg_score,
                    st.session_state.calculator.min_esg_score,
                    st.session_state.calculator.min_msci_score
                )
                
                assets_data.append({
                    "ID": asset.asset_id,
                    "Name": asset.name,
                    "Value (€M)": asset.market_value,
                    "EPC": asset.epc_rating or "-",
                    "Top 15%": "Yes" if asset.top_15_percent else "No",
                    "NZEB": "Yes" if asset.nzeb_compliant else "No",
                    "SDG Score": asset.un_sdg_score or "-",
                    "ESG Score": asset.esg_score or "-",
                    "DNSH": "Yes" if asset.dnsh_compliant else "No",
                    "Sustainable": "Yes" if is_sustainable else "No",
                    "Actions": i
                })
            
            df = pd.DataFrame(assets_data)
            st.dataframe(df.drop(columns=["Actions"]), use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                asset_to_edit = st.number_input(
                    "Select asset to edit (row number)",
                    min_value=0,
                    max_value=len(sci.assets)-1,
                    value=0
                )
            
            with col2:
                if st.button("Delete Selected Asset from SCI"):
                    sci.assets.pop(asset_to_edit)
                    st.success("Asset deleted from SCI successfully!")
                    update_calculator()
                    st.experimental_rerun()
            
            # Form to edit the selected asset in the SCI
            st.subheader(f"Edit Asset in {sci.name}")
            selected_asset = sci.assets[asset_to_edit]
            
            col1, col2 = st.columns(2)
            
            with col1:
                asset_id = st.text_input(f"Asset ID for {sci.name}", value=selected_asset.asset_id)
                asset_name = st.text_input(f"Asset Name for {sci.name}", value=selected_asset.name)
                market_value = st.number_input(f"Market Value (€M) for {sci.name}", value=selected_asset.market_value, step=0.1)
                epc_rating = st.selectbox(
                    f"EPC Rating for {sci.name}",
                    ["", "A", "B", "C", "D", "E", "F", "G"],
                    index=0 if not selected_asset.epc_rating else ["", "A", "B", "C", "D", "E", "F", "G"].index(selected_asset.epc_rating)
                )
                top_15_percent = st.checkbox(f"In Top 15% of Building Stock for {sci.name}", value=selected_asset.top_15_percent)
            
            with col2:
                nzeb_compliant = st.checkbox(f"NZEB -10% Compliant for {sci.name}", value=selected_asset.nzeb_compliant)
                un_sdg_score = st.slider(
                    f"UN SDG Score (0-10) for {sci.name}",
                    min_value=0.0,
                    max_value=10.0,
                    value=selected_asset.un_sdg_score if selected_asset.un_sdg_score is not None else 0.0,
                    step=0.1
                )
                esg_score = st.slider(
                    f"ESG Score (0-20) for {sci.name}",
                    min_value=0.0,
                    max_value=20.0,
                    value=selected_asset.esg_score if selected_asset.esg_score is not None else 0.0,
                    step=0.1
                )
                dnsh_compliant = st.checkbox(f"DNSH Compliant for {sci.name}", value=selected_asset.dnsh_compliant)
            
            st.subheader(f"Renovation Information for {sci.name} (if applicable)")
            col1, col2 = st.columns(2)
            
            with col1:
                renovation_energy = st.number_input(
                    f"Renovation Energy Reduction (%) for {sci.name}",
                    min_value=0.0,
                    max_value=100.0,
                    value=selected_asset.renovation_energy_reduction if selected_asset.renovation_energy_reduction is not None else 0.0,
                    step=0.1
                )
            
            with col2:
                renovation_ghg = st.number_input(
                    f"Renovation GHG Reduction (%) for {sci.name}",
                    min_value=0.0,
                    max_value=100.0,
                    value=selected_asset.renovation_ghg_reduction if selected_asset.renovation_ghg_reduction is not None else 0.0,
                    step=0.1
                )
            
            if st.button(f"Save Asset in {sci.name}"):
                updated_asset = Asset(
                    asset_id=asset_id,
                    name=asset_name,
                    market_value=market_value,
                    epc_rating=epc_rating if epc_rating else None,
                    top_15_percent=top_15_percent,
                    nzeb_compliant=nzeb_compliant,
                    renovation_energy_reduction=renovation_energy if renovation_energy > 0 else None,
                    renovation_ghg_reduction=renovation_ghg if renovation_ghg > 0 else None,
                    un_sdg_score=un_sdg_score if un_sdg_score > 0 else None,
                    esg_score=esg_score if esg_score > 0 else None,
                    msci_score=None,
                    dnsh_compliant=dnsh_compliant
                )
                
                sci.assets[asset_to_edit] = updated_asset
                st.success(f"Asset updated in {sci.name} successfully!")
                update_calculator()
                st.experimental_rerun()
        
        # Add new asset to the SCI
        st.subheader(f"Add New Asset to {sci.name}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_asset_id = st.text_input(f"New Asset ID for {sci.name}", value=f"{sci.sci_id}-A{len(sci.assets)+1}")
            new_asset_name = st.text_input(f"New Asset Name for {sci.name}")
            new_market_value = st.number_input(f"New Market Value (€M) for {sci.name}", value=0.0, step=0.1)
            new_epc_rating = st.selectbox(
                f"New EPC Rating for {sci.name}",
                ["", "A", "B", "C", "D", "E", "F", "G"],
                index=0
            )
            new_top_15_percent = st.checkbox(f"New Asset In Top 15% of Building Stock for {sci.name}")
        
        with col2:
            new_nzeb_compliant = st.checkbox(f"New Asset NZEB -10% Compliant for {sci.name}")
            new_un_sdg_score = st.slider(
                f"New Asset UN SDG Score (0-10) for {sci.name}",
                min_value=0.0,
                max_value=10.0,
                value=0.0,
                step=0.1
            )
            new_esg_score = st.slider(
                f"New Asset ESG Score (0-20) for {sci.name}",
                min_value=0.0,
                max_value=20.0,
                value=0.0,
                step=0.1
            )
            new_dnsh_compliant = st.checkbox(f"New Asset DNSH Compliant for {sci.name}")
        
        st.subheader(f"New Asset Renovation Information for {sci.name} (if applicable)")
        col1, col2 = st.columns(2)
        
        with col1:
            new_renovation_energy = st.number_input(
                f"New Asset Renovation Energy Reduction (%) for {sci.name}",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1
            )
        
        with col2:
            new_renovation_ghg = st.number_input(
                f"New Asset Renovation GHG Reduction (%) for {sci.name}",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1
            )
        
        if st.button(f"Add Asset to {sci.name}"):
            new_asset = Asset(
                asset_id=new_asset_id,
                name=new_asset_name,
                market_value=new_market_value,
                epc_rating=new_epc_rating if new_epc_rating else None,
                top_15_percent=new_top_15_percent,
                nzeb_compliant=new_nzeb_compliant,
                renovation_energy_reduction=new_renovation_energy if new_renovation_energy > 0 else None,
                renovation_ghg_reduction=new_renovation_ghg if new_renovation_ghg > 0 else None,
                un_sdg_score=new_un_sdg_score if new_un_sdg_score > 0 else None,
                esg_score=new_esg_score if new_esg_score > 0 else None,
                msci_score=None,
                dnsh_compliant=new_dnsh_compliant
            )
            
            sci.assets.append(new_asset)
            st.success(f"Asset added to {sci.name} successfully!")
            update_calculator()
            st.experimental_rerun()
    
    # Add new SCI form
    st.subheader("Add New SCI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_sci_id = st.text_input("SCI ID", value=f"SCI{len(st.session_state.scis)+1:03d}")
    
    with col2:
        new_sci_name = st.text_input("SCI Name")
    
    if st.button("Add New SCI"):
        if not new_sci_name:
            st.error("SCI Name is required")
        else:
            new_sci = SCI(
                sci_id=new_sci_id,
                name=new_sci_name,
                assets=[]
            )
            
            st.session_state.scis.append(new_sci)
            st.success("SCI added successfully!")
            update_calculator()
            st.experimental_rerun()

def display_controlled_participations():
    """Display and manage controlled participations (>50%)."""
    st.header("Controlled Participations (>50%)")
    
    # Display existing controlled participations
    if st.session_state.controlled_participations:
        st.subheader("Existing Controlled Participations")
        
        participations_data = []
        for i, participation in enumerate(st.session_state.controlled_participations):
            participations_data.append({
                "ID": participation.vehicle_id,
                "Name": participation.name,
                "Ownership %": f"{participation.ownership_percentage:.2f}%",
                "Total Value (€M)": participation.total_value,
                "Sustainable %": f"{participation.sustainable_percentage:.2f}%",
                "Sustainable Value (€M)": participation.sustainable_value(),
                "Actions": i
            })
        
        df = pd.DataFrame(participations_data)
        st.dataframe(df.drop(columns=["Actions"]), use_container_width=True)
        
        # Action buttons for each participation
        col1, col2 = st.columns(2)
        with col1:
            participation_to_edit = st.number_input(
                "Select participation to edit (row number)",
                min_value=0,
                max_value=len(st.session_state.controlled_participations)-1 if st.session_state.controlled_participations else 0,
                value=0
            )
        
        with col2:
            if st.button("Delete Selected Participation") and st.session_state.controlled_participations:
                st.session_state.controlled_participations.pop(participation_to_edit)
                st.success("Participation deleted successfully!")
                update_calculator()
                st.experimental_rerun()
    
    # Form to add or edit a participation
    st.subheader("Add New Controlled Participation" if not st.session_state.controlled_participations else "Add/Edit Controlled Participation")
    
    participation_to_add = Participation(
        vehicle_id="",
        name="",
        ownership_percentage=51.0,
        total_value=0.0,
        sustainable_percentage=0.0
    )
    
    # If editing, pre-fill the form with the selected participation's values
    if st.session_state.controlled_participations and participation_to_edit is not None and participation_to_edit < len(st.session_state.controlled_participations):
        participation_to_add = st.session_state.controlled_participations[participation_to_edit]
    
    col1, col2 = st.columns(2)
    
    with col1:
        vehicle_id = st.text_input("Vehicle ID", value=participation_to_add.vehicle_id)
        vehicle_name = st.text_input("Vehicle Name", value=participation_to_add.name)
    
    with col2:
        ownership_percentage = st.slider(
            "Ownership Percentage (%)",
            min_value=50.1,
            max_value=100.0,
            value=participation_to_add.ownership_percentage,
            step=0.1
        )
        total_value = st.number_input("Total Vehicle Value (€M)", value=participation_to_add.total_value, step=0.1)
        sustainable_percentage = st.slider(
            "Sustainable Percentage (%)",
            min_value=0.0,
            max_value=100.0,
            value=participation_to_add.sustainable_percentage,
            step=0.1
        )
    
    if st.button("Save Controlled Participation"):
        new_participation = Participation(
            vehicle_id=vehicle_id,
            name=vehicle_name,
            ownership_percentage=ownership_percentage,
            total_value=total_value,
            sustainable_percentage=sustainable_percentage
        )
        
        if (st.session_state.controlled_participations and 
            participation_to_edit is not None and 
            participation_to_edit < len(st.session_state.controlled_participations)):
            # Update existing participation
            st.session_state.controlled_participations[participation_to_edit] = new_participation
            st.success("Participation updated successfully!")
        else:
            # Add new participation
            st.session_state.controlled_participations.append(new_participation)
            st.success("Participation added successfully!")
        
        update_calculator()
        st.experimental_rerun()

def display_uncontrolled_participations():
    """Display and manage uncontrolled participations (20-50%)."""
    st.header("Uncontrolled Participations (20-50%)")
    
    # Display existing uncontrolled participations
    if st.session_state.uncontrolled_participations:
        st.subheader("Existing Uncontrolled Participations")
        
        participations_data = []
        for i, participation in enumerate(st.session_state.uncontrolled_participations):
            participations_data.append({
                "ID": participation.vehicle_id,
                "Name": participation.name,
                "Ownership %": f"{participation.ownership_percentage:.2f}%",
                "Total Value (€M)": participation.total_value,
                "Ownership-Adj. Value (€M)": participation.ownership_adjusted_value(),
                "Sustainable %": f"{participation.sustainable_percentage:.2f}%",
                "Sustainable Value (€M)": participation.ownership_adjusted_sustainable_value(),
                "Actions": i
            })
        
        df = pd.DataFrame(participations_data)
        st.dataframe(df.drop(columns=["Actions"]), use_container_width=True)
        
        # Action buttons for each participation
        col1, col2 = st.columns(2)
        with col1:
            participation_to_edit = st.number_input(
                "Select participation to edit (row number)",
                min_value=0,
                max_value=len(st.session_state.uncontrolled_participations)-1 if st.session_state.uncontrolled_participations else 0,
                value=0
            )
        
        with col2:
            if st.button("Delete Selected Participation") and st.session_state.uncontrolled_participations:
                st.session_state.uncontrolled_participations.pop(participation_to_edit)
                st.success("Participation deleted successfully!")
                update_calculator()
                st.experimental_rerun()
    
    # Form to add or edit a participation
    st.subheader("Add New Uncontrolled Participation" if not st.session_state.uncontrolled_participations else "Add/Edit Uncontrolled Participation")
    
    participation_to_add = Participation(
        vehicle_id="",
        name="",
        ownership_percentage=30.0,
        total_value=0.0,
        sustainable_percentage=0.0
    )
    
    # If editing, pre-fill the form with the selected participation's values
    if st.session_state.uncontrolled_participations and participation_to_edit is not None and participation_to_edit < len(st.session_state.uncontrolled_participations):
        participation_to_add = st.session_state.uncontrolled_participations[participation_to_edit]
    
    col1, col2 = st.columns(2)
    
    with col1:
        vehicle_id = st.text_input("Vehicle ID", value=participation_to_add.vehicle_id)
        vehicle_name = st.text_input("Vehicle Name", value=participation_to_add.name)
    
    with col2:
        ownership_percentage = st.slider(
            "Ownership Percentage (%)",
            min_value=20.0,
            max_value=50.0,
            value=participation_to_add.ownership_percentage,
            step=0.1
        )
        total_value = st.number_input("Total Vehicle Value (€M)", value=participation_to_add.total_value, step=0.1)
        sustainable_percentage = st.slider(
            "Sustainable Percentage (%)",
            min_value=0.0,
            max_value=100.0,
            value=participation_to_add.sustainable_percentage,
            step=0.1
        )
    
    if st.button("Save Uncontrolled Participation"):
        new_participation = Participation(
            vehicle_id=vehicle_id,
            name=vehicle_name,
            ownership_percentage=ownership_percentage,
            total_value=total_value,
            sustainable_percentage=sustainable_percentage
        )
        
        if (st.session_state.uncontrolled_participations and 
            participation_to_edit is not None and 
            participation_to_edit < len(st.session_state.uncontrolled_participations)):
            # Update existing participation
            st.session_state.uncontrolled_participations[participation_to_edit] = new_participation
            st.success("Participation updated successfully!")
        else:
            # Add new participation
            st.session_state.uncontrolled_participations.append(new_participation)
            st.success("Participation added successfully!")
        
        update_calculator()
        st.experimental_rerun()

def display_minority_stakes():
    """Display and manage minority stakes (<20%)."""
    st.header("Minority Stakes (<20%)")
    
    # Display existing minority stakes
    if st.session_state.minority_stakes:
        st.subheader("Existing Minority Stakes")
        
        stakes_data = []
        for i, stake in enumerate(st.session_state.minority_stakes):
            stakes_data.append({
                "ID": stake.vehicle_id,
                "Name": stake.name,
                "Ownership %": f"{stake.ownership_percentage:.2f}%",
                "Total Value (€M)": stake.total_value,
                "Ownership-Adj. Value (€M)": stake.ownership_adjusted_value(),
                "Sustainable %": f"{stake.sustainable_percentage:.2f}%",
                "Sustainable Value (€M)": stake.ownership_adjusted_sustainable_value(),
                "Actions": i
            })
        
        df = pd.DataFrame(stakes_data)
        st.dataframe(df.drop(columns=["Actions"]), use_container_width=True)
        
        # Action buttons for each stake
        col1, col2 = st.columns(2)
        with col1:
            stake_to_edit = st.number_input(
                "Select stake to edit (row number)",
                min_value=0,
                max_value=len(st.session_state.minority_stakes)-1 if st.session_state.minority_stakes else 0,
                value=0
            )
        
        with col2:
            if st.button("Delete Selected Stake") and st.session_state.minority_stakes:
                st.session_state.minority_stakes.pop(stake_to_edit)
                st.success("Minority stake deleted successfully!")
                update_calculator()
                st.experimental_rerun()
    
    # Form to add or edit a stake
    st.subheader("Add New Minority Stake" if not st.session_state.minority_stakes else "Add/Edit Minority Stake")
    
    stake_to_add = Participation(
        vehicle_id="",
        name="",
        ownership_percentage=10.0,
        total_value=0.0,
        sustainable_percentage=0.0
    )
    
    # If editing, pre-fill the form with the selected stake's values
    if st.session_state.minority_stakes and stake_to_edit is not None and stake_to_edit < len(st.session_state.minority_stakes):
        stake_to_add = st.session_state.minority_stakes[stake_to_edit]
    
    col1, col2 = st.columns(2)
    
    with col1:
        vehicle_id = st.text_input("Vehicle ID", value=stake_to_add.vehicle_id)
        vehicle_name = st.text_input("Vehicle Name", value=stake_to_add.name)
    
    with col2:
        ownership_percentage = st.slider(
            "Ownership Percentage (%)",
            min_value=0.1,
            max_value=19.9,
            value=stake_to_add.ownership_percentage,
            step=0.1
        )
        total_value = st.number_input("Total Vehicle Value (€M)", value=stake_to_add.total_value, step=0.1)
        sustainable_percentage = st.slider(
            "Sustainable Percentage (%)",
            min_value=0.0,
            max_value=100.0,
            value=stake_to_add.sustainable_percentage,
            step=0.1
        )
    
    if st.button("Save Minority Stake"):
        new_stake = Participation(
            vehicle_id=vehicle_id,
            name=vehicle_name,
            ownership_percentage=ownership_percentage,
            total_value=total_value,
            sustainable_percentage=sustainable_percentage
        )
        
        if (st.session_state.minority_stakes and 
            stake_to_edit is not None and 
            stake_to_edit < len(st.session_state.minority_stakes)):
            # Update existing stake
            st.session_state.minority_stakes[stake_to_edit] = new_stake
            st.success("Minority stake updated successfully!")
        else:
            # Add new stake
            st.session_state.minority_stakes.append(new_stake)
            st.success("Minority stake added successfully!")
        
        update_calculator()
        st.experimental_rerun()

def display_pe_fund_participations():
    """Display and manage PE fund participations."""
    st.header("PE Fund Participations")
    
    # Display existing PE fund participations
    if st.session_state.pe_fund_participations:
        st.subheader("Existing PE Fund Participations")
        
        pe_funds_data = []
        for i, pe_fund in enumerate(st.session_state.pe_fund_participations):
            pe_funds_data.append({
                "ID": pe_fund.fund_id,
                "Name": pe_fund.name,
                "Investment Value (€M)": pe_fund.investment_value,
                "Sustainable %": f"{pe_fund.estimated_sustainable_percentage:.2f}%",
                "Sustainable Value (€M)": pe_fund.sustainable_value(),
                "Estimation Method": pe_fund.estimation_method,
                "Actions": i
            })
        
        df = pd.DataFrame(pe_funds_data)
        st.dataframe(df.drop(columns=["Actions"]), use_container_width=True)
        
        # Action buttons for each PE fund
        col1, col2 = st.columns(2)
        with col1:
            pe_fund_to_edit = st.number_input(
                "Select PE fund to edit (row number)",
                min_value=0,
                max_value=len(st.session_state.pe_fund_participations)-1 if st.session_state.pe_fund_participations else 0,
                value=0
            )
        
        with col2:
            if st.button("Delete Selected PE Fund") and st.session_state.pe_fund_participations:
                st.session_state.pe_fund_participations.pop(pe_fund_to_edit)
                st.success("PE fund deleted successfully!")
                update_calculator()
                st.experimental_rerun()
    
    # Form to add or edit a PE fund
    st.subheader("Add New PE Fund" if not st.session_state.pe_fund_participations else "Add/Edit PE Fund")
    
    pe_fund_to_add = PEFundParticipation(
        fund_id="",
        name="",
        investment_value=0.0,
        estimated_sustainable_percentage=0.0,
        estimation_method=""
    )
    
    # If editing, pre-fill the form with the selected PE fund's values
    if st.session_state.pe_fund_participations and pe_fund_to_edit is not None and pe_fund_to_edit < len(st.session_state.pe_fund_participations):
        pe_fund_to_add = st.session_state.pe_fund_participations[pe_fund_to_edit]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fund_id = st.text_input("PE Fund ID", value=pe_fund_to_add.fund_id)
        fund_name = st.text_input("PE Fund Name", value=pe_fund_to_add.name)
        investment_value = st.number_input("Investment Value (€M)", value=pe_fund_to_add.investment_value, step=0.1)
    
    with col2:
        estimated_sustainable_percentage = st.slider(
            "Estimated Sustainable Percentage (%)",
            min_value=0.0,
            max_value=100.0,
            value=pe_fund_to_add.estimated_sustainable_percentage,
            step=0.1
        )
        estimation_method = st.text_area(
            "Estimation Method",
            value=pe_fund_to_add.estimation_method,
            height=100
        )
    
    if st.button("Save PE Fund"):
        new_pe_fund = PEFundParticipation(
            fund_id=fund_id,
            name=fund_name,
            investment_value=investment_value,
            estimated_sustainable_percentage=estimated_sustainable_percentage,
            estimation_method=estimation_method
        )
        
        if (st.session_state.pe_fund_participations and 
            pe_fund_to_edit is not None and 
            pe_fund_to_edit < len(st.session_state.pe_fund_participations)):
            # Update existing PE fund
            st.session_state.pe_fund_participations[pe_fund_to_edit] = new_pe_fund
            st.success("PE fund updated successfully!")
        else:
            # Add new PE fund
            st.session_state.pe_fund_participations.append(new_pe_fund)
            st.success("PE fund added successfully!")
        
        update_calculator()
        st.experimental_rerun()

def update_calculator():
    """Update the calculator with the current session state data."""
    calculator = st.session_state.calculator
    
    # Clear existing assets and participations
    calculator.direct_assets = []
    calculator.scis = []
    calculator.controlled_participations = []
    calculator.uncontrolled_participations = []
    calculator.minority_stakes = []
    calculator.pe_fund_participations = []
    
    # Add direct assets
    for asset in st.session_state.direct_assets:
        calculator.add_direct_asset(asset)
    
    # Add SCIs
    for sci in st.session_state.scis:
        calculator.add_sci(sci)
    
    # Add controlled participations
    for participation in st.session_state.controlled_participations:
        calculator.add_controlled_participation(participation)
    
    # Add uncontrolled participations
    for participation in st.session_state.uncontrolled_participations:
        calculator.add_uncontrolled_participation(participation)
    
    # Add minority stakes
    for stake in st.session_state.minority_stakes:
        calculator.add_minority_stake(stake)
    
    # Add PE fund participations
    for pe_fund in st.session_state.pe_fund_participations:
        calculator.add_pe_fund_participation(pe_fund)

def load_sample_data():
    """Load sample data for demonstration purposes."""
    # Clear existing data
    st.session_state.direct_assets = []
    st.session_state.scis = []
    st.session_state.controlled_participations = []
    st.session_state.uncontrolled_participations = []
    st.session_state.minority_stakes = []
    st.session_state.pe_fund_participations = []
    
    # Set fund information
    st.session_state.calculator = SustainableRealEstateCalculator(
        fund_name="Green Real Estate Fund",
        fund_type="Article 8",
        reporting_date="2024-12-31"
    )
    
    # Add direct assets
    st.session_state.direct_assets = [
        Asset(
            asset_id="DA001",
            name="Office Paris",
            market_value=25.0,
            epc_rating="A",
            top_15_percent=True,
            un_sdg_score=7.5,
            esg_score=15.0,
            dnsh_compliant=True
        ),
        Asset(
            asset_id="DA002",
            name="Retail Lyon",
            market_value=15.0,
            epc_rating="B",
            top_15_percent=False,
            un_sdg_score=6.0,
            esg_score=14.0,
            dnsh_compliant=True
        ),
        Asset(
            asset_id="DA003",
            name="Logistics Lille",
            market_value=18.0,
            epc_rating="C",
            top_15_percent=False,
            un_sdg_score=2.0,
            esg_score=10.0,
            dnsh_compliant=True
        ),
        Asset(
            asset_id="DA004",
            name="Office Bordeaux",
            market_value=12.0,
            epc_rating="B",
            top_15_percent=True,
            un_sdg_score=5.5,
            esg_score=16.0,
            dnsh_compliant=True
        ),
        Asset(
            asset_id="DA005",
            name="Hotel Marseille",
            market_value=20.0,
            epc_rating="D",
            top_15_percent=False,
            un_sdg_score=3.0,
            esg_score=7.0,
            dnsh_compliant=False
        )
    ]
    
    # Add SCIs
    st.session_state.scis = [
        SCI(
            sci_id="SCI001",
            name="SCI-1",
            assets=[
                Asset(
                    asset_id="SCI1-A1",
                    name="Office Strasbourg",
                    market_value=14.0,
                    epc_rating="A",
                    top_15_percent=True,
                    un_sdg_score=8.0,
                    esg_score=17.0,
                    dnsh_compliant=True
                ),
                Asset(
                    asset_id="SCI1-A2",
                    name="Retail Nantes",
                    market_value=10.0,
                    epc_rating="C",
                    top_15_percent=False,
                    renovation_energy_reduction=35.0,
                    un_sdg_score=4.0,
                    esg_score=12.0,
                    dnsh_compliant=True
                ),
                Asset(
                    asset_id="SCI1-A3",
                    name="Warehouse Toulouse",
                    market_value=8.0,
                    epc_rating="B",
                    top_15_percent=True,
                    un_sdg_score=5.5,
                    esg_score=13.0,
                    dnsh_compliant=True
                )
            ]
        ),
        SCI(
            sci_id="SCI002",
            name="SCI-2",
            assets=[
                Asset(
                    asset_id="SCI2-A1",
                    name="Office Rennes",
                    market_value=12.0,
                    epc_rating="B",
                    top_15_percent=False,
                    renovation_ghg_reduction=32.0,
                    un_sdg_score=6.0,
                    esg_score=14.0,
                    dnsh_compliant=True
                ),
                Asset(
                    asset_id="SCI2-A2",
                    name="Retail Montpellier",
                    market_value=8.0,
                    epc_rating="D",
                    top_15_percent=False,
                    un_sdg_score=2.0,
                    esg_score=9.0,
                    dnsh_compliant=False
                )
            ]
        )
    ]
    
    # Add controlled participation
    st.session_state.controlled_participations = [
        Participation(
            vehicle_id="CP001",
            name="Green Office OPCI",
            ownership_percentage=75.0,
            total_value=60.0,
            sustainable_percentage=70.0
        )
    ]
    
    # Add uncontrolled participations
    st.session_state.uncontrolled_participations = [
        Participation(
            vehicle_id="UP001",
            name="Retail SCPI",
            ownership_percentage=30.0,
            total_value=40.0,
            sustainable_percentage=65.0
        ),
        Participation(
            vehicle_id="UP002",
            name="Eco-Logistics Fund",
            ownership_percentage=25.0,
            total_value=30.0,
            sustainable_percentage=80.0
        )
    ]
    
    # Add minority stake
    st.session_state.minority_stakes = [
        Participation(
            vehicle_id="MS001",
            name="Urban Renewal Fund",
            ownership_percentage=10.0,
            total_value=25.0,
            sustainable_percentage=55.0
        )
    ]
    
    # Add PE fund participation
    st.session_state.pe_fund_participations = [
        PEFundParticipation(
            fund_id="PEF001",
            name="Green Infrastructure PE",
            investment_value=20.0,
            estimated_sustainable_percentage=60.0,
            estimation_method="Based on fund manager's report"
        )
    ]
    
    # Update calculator
    update_calculator()

if __name__ == "__main__":
    main()