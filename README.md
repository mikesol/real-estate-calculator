# Sustainable Real Estate Investment Calculator

This repository provides tools for calculating sustainable investment percentages in real estate portfolios, following EU Taxonomy, SFDR, and industry guidelines from ASPIM and AMF.

## Overview

This calculator helps real estate fund managers determine:
- What percentage of investments qualify as "sustainable" under regulatory frameworks
- EU Taxonomy alignment percentages
- Compliance with SFDR Article 8/9 requirements

## Calculation Methodology

### Asset Eligibility Criteria

For an asset to qualify as sustainable, it must meet all three conditions:

1. **Positive Environmental/Social Contribution**
   - Minimum score of 2.5/10 on UN SDG alignment scale

2. **Do No Significant Harm (DNSH) Principle**
   - Compliance with all applicable DNSH criteria
   - No significant negative impacts on other environmental objectives

3. **Good Governance**
   - Minimum score of 8/20 on internal ESG rating OR
   - Minimum score of 4/10 on MSCI rating

### Real Estate Technical Screening Criteria

Buildings must satisfy at least one of these thresholds:

1. **Energy Performance**
   - EPC Class A rating OR
   - Within top 15% of national/regional building stock (for buildings built before 2020)

2. **New Buildings (post-2020)**
   - NZEB -10% (Nearly Zero Energy Building minus 10%)

3. **Renovation Impact**
   - 30% reduction in primary energy demand OR
   - 30% reduction in GHG emissions compared to initial performance

### Fund Structure Calculation Rules

| Investment Type | Calculation Approach |
|----------------|----------------------|
| Direct assets | 100% inclusion when meeting all criteria |
| SCIs (100% owned) | Full look-through approach |
| Controlled participations (>50%) | Full consolidation |
| Uncontrolled participations (20-50%) | Proportional calculation based on ownership % |
| Minority stakes (<20%) | Based on available data or sectoral averages |
| PE fund participations | Best-effort estimations |

## How to Use the Calculator

### Python Module

1. Clone this repository
2. Import the `SustainableRealEstateCalculator` class from `sustainable_calculator.py`
3. Create calculator instances and add your assets and investments
4. Call `calculate_total()` to get the sustainability metrics

```python
from sustainable_calculator import SustainableRealEstateCalculator, Asset

calculator = SustainableRealEstateCalculator(
    fund_name="My Fund",
    fund_type="Article 8",
    reporting_date="2024-01-01"
)

# Add your assets and investments
calculator.add_direct_asset(Asset(...))

# Calculate results
results = calculator.calculate_total()
```

### Streamlit Web Application

We provide an interactive Streamlit web application for easier data input and visualization:

1. Clone this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```
4. Access the app in your browser at `http://localhost:8501`
5. Use the sidebar to navigate between sections
6. Input your fund data, or click "Load Sample Data" for a demonstration
7. View the dashboard for calculation results and visualizations
8. Download the report in JSON format for your records

## Example

See `EXAMPLE.md` and `example.xlsx` for a detailed walkthrough with a sample fund structure.

## Regulatory Compliance

This calculator follows:
- EU Taxonomy framework
- SFDR Article 8/9 requirements
- ASPIM and AMF guidelines for sustainable real estate

## Documents

This repository contains reference documents:
- EU Commission guidelines
- ASPIM position papers
- Industry methodologies (including Rothschild approach)