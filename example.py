"""
Example usage of the Sustainable Real Estate Calculator

This example demonstrates calculating sustainable investment percentages
for a sample fund with various investment types.
"""

from sustainable_calculator import (
    SustainableRealEstateCalculator,
    Asset,
    SCI,
    Participation,
    PEFundParticipation
)

def main():
    """Main function to demonstrate calculator usage."""
    # Initialize calculator with fund information
    calculator = SustainableRealEstateCalculator(
        fund_name="Green Real Estate Fund",
        fund_type="Article 8",
        reporting_date="2024-12-31"
    )
    
    # Add direct assets
    calculator.add_direct_asset(Asset(
        asset_id="DA001",
        name="Office Paris",
        market_value=25.0,
        epc_rating="A",
        top_15_percent=True,
        un_sdg_score=7.5,
        esg_score=15.0,
        dnsh_compliant=True
    ))
    
    calculator.add_direct_asset(Asset(
        asset_id="DA002",
        name="Retail Lyon",
        market_value=15.0,
        epc_rating="B",
        top_15_percent=False,
        un_sdg_score=6.0,
        esg_score=14.0,
        dnsh_compliant=True
    ))
    
    calculator.add_direct_asset(Asset(
        asset_id="DA003",
        name="Logistics Lille",
        market_value=18.0,
        epc_rating="C",
        top_15_percent=False,
        un_sdg_score=2.0,
        esg_score=10.0,
        dnsh_compliant=True
    ))
    
    calculator.add_direct_asset(Asset(
        asset_id="DA004",
        name="Office Bordeaux",
        market_value=12.0,
        epc_rating="B",
        top_15_percent=True,
        un_sdg_score=5.5,
        esg_score=16.0,
        dnsh_compliant=True
    ))
    
    calculator.add_direct_asset(Asset(
        asset_id="DA005",
        name="Hotel Marseille",
        market_value=20.0,
        epc_rating="D",
        top_15_percent=False,
        un_sdg_score=3.0,
        esg_score=7.0,
        dnsh_compliant=False
    ))
    
    # Add SCIs (100% owned)
    # SCI-1
    sci_1 = SCI(
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
    )
    calculator.add_sci(sci_1)
    
    # SCI-2
    sci_2 = SCI(
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
    calculator.add_sci(sci_2)
    
    # Add controlled participation (>50%)
    calculator.add_controlled_participation(Participation(
        vehicle_id="CP001",
        name="Green Office OPCI",
        ownership_percentage=75.0,
        total_value=60.0,
        sustainable_percentage=70.0
    ))
    
    # Add uncontrolled participations (20-50%)
    calculator.add_uncontrolled_participation(Participation(
        vehicle_id="UP001",
        name="Retail SCPI",
        ownership_percentage=30.0,
        total_value=40.0,
        sustainable_percentage=65.0
    ))
    
    calculator.add_uncontrolled_participation(Participation(
        vehicle_id="UP002",
        name="Eco-Logistics Fund",
        ownership_percentage=25.0,
        total_value=30.0,
        sustainable_percentage=80.0
    ))
    
    # Add minority stake (<20%)
    calculator.add_minority_stake(Participation(
        vehicle_id="MS001",
        name="Urban Renewal Fund",
        ownership_percentage=10.0,
        total_value=25.0,
        sustainable_percentage=55.0
    ))
    
    # Add PE fund participation
    calculator.add_pe_fund_participation(PEFundParticipation(
        fund_id="PEF001",
        name="Green Infrastructure PE",
        investment_value=20.0,
        estimated_sustainable_percentage=60.0,
        estimation_method="Based on fund manager's report"
    ))
    
    # Generate and print the calculation report
    results = calculator.calculate_total()
    print_results(results)

def print_results(results):
    """Print the calculation results in a formatted way."""
    print("\n" + "=" * 80)
    print(f"SUSTAINABLE REAL ESTATE CALCULATION RESULTS: {results['fund_info']['fund_name']}")
    print(f"Fund Type: {results['fund_info']['fund_type']} | Reporting Date: {results['fund_info']['reporting_date']}")
    print("=" * 80)
    
    print("\nINVESTMENT CATEGORY BREAKDOWN:")
    print("-" * 80)
    print(f"{'Category':<30} {'Total Value (€M)':<20} {'Sustainable (€M)':<20} {'Sustainable %':<15}")
    print("-" * 80)
    
    categories = [
        ("Direct Assets", results["direct_assets"]),
        ("100% Owned SCIs", results["scis"]),
        ("Controlled Participations", results["controlled_participations"]),
        ("Uncontrolled Participations", results["uncontrolled_participations"]),
        ("Minority Stakes", results["minority_stakes"]),
        ("PE Fund Participations", results["pe_fund_participations"]),
    ]
    
    for name, category in categories:
        print(f"{name:<30} {category['total_value']:<20.2f} {category['sustainable_value']:<20.2f} {category['sustainable_percentage']:<15.2f}%")
    
    print("-" * 80)
    print(f"{'FUND TOTAL':<30} {results['fund_total']['total_value']:<20.2f} {results['fund_total']['sustainable_value']:<20.2f} {results['fund_total']['sustainable_percentage']:<15.2f}%")
    print("-" * 80)
    
    # Print sustainability assessment
    sustainable_percentage = results['fund_total']['sustainable_percentage']
    print("\nSUSTAINABILITY ASSESSMENT:")
    if sustainable_percentage >= 75:
        print("High sustainable investment proportion (>75%)")
    elif sustainable_percentage >= 50:
        print("Substantial sustainable investment proportion (50-75%)")
    elif sustainable_percentage >= 20:
        print("Moderate sustainable investment proportion (20-50%)")
    else:
        print("Limited sustainable investment proportion (<20%)")
    
    # Print regulatory classification suggestion
    print("\nREGULATORY CLASSIFICATION GUIDANCE:")
    if sustainable_percentage >= 50:
        print("- Qualifies for Article 8 with sustainable investments")
        if sustainable_percentage >= 80:
            print("- May consider Article 9 classification (if environmental/social objective is the target)")
    elif sustainable_percentage >= 20:
        print("- Qualifies for Article 8")
    else:
        print("- Consider Article 6 classification")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()