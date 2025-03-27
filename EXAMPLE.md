# Sustainable Real Estate Calculator: Example Use Case

This document demonstrates how to use the sustainable real estate calculator for a sample fund with various investment types.

## Example Fund Structure

Our example fund has the following structure:

```
Green Real Estate Fund (Article 8)
├── 5 Direct Assets
│   ├── Office Paris
│   ├── Retail Lyon
│   ├── Logistics Lille
│   ├── Office Bordeaux
│   └── Hotel Marseille
├── 2 SCIs (100% owned)
│   ├── SCI-1
│   │   ├── Office Strasbourg
│   │   ├── Retail Nantes
│   │   └── Warehouse Toulouse
│   └── SCI-2
│       ├── Office Rennes
│       └── Retail Montpellier
├── 1 Controlled Participation (75% ownership)
│   └── Green Office OPCI
├── 2 Uncontrolled Participations
│   ├── Retail SCPI (30% ownership)
│   └── Eco-Logistics Fund (25% ownership)
├── 1 Minority Stake (10% ownership)
│   └── Urban Renewal Fund
└── 1 PE Fund Participation
    └── Green Infrastructure PE
```

## Running the Example

To run the example, simply execute:

```bash
python example.py
```

## Code Walkthrough

The example demonstrates how to:

1. Initialize the calculator with fund information
2. Add direct assets with sustainability criteria
3. Add SCIs (100% owned) with their own assets
4. Add various participation types with different ownership percentages
5. Calculate and display the results

## Calculation Logic Overview

The calculator follows these principles:

### Asset Eligibility Assessment

For an individual asset to qualify as sustainable, it must meet ALL three conditions:

1. **Positive contribution**: UN SDG score ≥ 2.5/10
2. **DNSH compliance**: Do No Significant Harm principle
3. **Good governance**: ESG score ≥ 8/20 or MSCI score ≥ 4/10

Additionally, it must meet at least ONE technical criterion:
- EPC Class A rating OR
- In top 15% of building stock OR
- NZEB -10% compliance OR
- 30% reduction in energy demand/GHG emissions

### Investment Structure Handling

- **Direct assets**: 100% inclusion when meeting all criteria
- **SCIs (100% owned)**: Full look-through approach, assessing each underlying asset
- **Controlled participations (>50%)**: Full consolidation of sustainable value
- **Uncontrolled participations (20-50%)**: Proportional calculation based on ownership %
- **Minority stakes (<20%)**: Proportional calculation based on ownership %
- **PE fund participations**: Based on best-effort estimation

## Example Results

Based on the example data, the fund achieves:

| Investment Category | Total Value (€M) | Sustainable Value (€M) | Sustainable % |
|---------------------|------------------|------------------------|---------------|
| Direct Assets | 90.0 | 52.0 | 57.8% |
| 100% Owned SCIs | 52.0 | 44.0 | 84.6% |
| Controlled Participations | 60.0 | 42.0 | 70.0% |
| Uncontrolled Participations | 19.5 | 13.8 | 70.8% |
| Minority Stakes | 2.5 | 1.4 | 55.0% |
| PE Fund Participations | 20.0 | 12.0 | 60.0% |
| **FUND TOTAL** | **244.0** | **165.2** | **67.7%** |

With a 67.7% sustainable investment proportion, this fund would qualify as an Article 8 fund with a substantial proportion of sustainable investments according to SFDR requirements.

## Extension and Customization

The calculator can be easily extended or customized by:

1. Adjusting the minimum thresholds for sustainability criteria
2. Adding new technical screening criteria as regulations evolve
3. Modifying the calculation approach for different investment structures
4. Enhancing the reporting functionality

## Validation Checks

When using the calculator in practice, verify:

1. All required sustainability criteria are applied correctly
2. Appropriate technical screening criteria are used for each building
3. Correct calculation methods are applied based on ownership structure
4. Consistent data sources are used for sustainability assessments

## Regulatory Framework and Standards

This calculator's methodology is based on the following regulatory frameworks and industry standards:

### Key Regulations

1. **EU Taxonomy (Regulation (EU) 2020/852)**
   - Technical Screening Criteria for buildings in Climate Delegated Act (EU) 2021/2139
   - Focus on climate change mitigation and adaptation objectives
   - Specific thresholds for building energy performance (EPC A, top 15%, NZEB-10%)

2. **Sustainable Finance Disclosure Regulation (SFDR) (Regulation (EU) 2019/2088)**
   - Article 8: Products promoting environmental/social characteristics
   - Article 9: Products with sustainable investment as their objective
   - Regulatory Technical Standards (RTS) on ESG disclosures (C(2022) 1931)

3. **French Regulatory Requirements**
   - AMF Position-Recommendation DOC-2020-03 on ESG approaches
   - Law on Energy and Climate (Article 29 LEC) disclosure requirements

### Industry Methodologies

- **ASPIM C-ISR** methodology for real estate funds
  - Fund classification approach based on ASPIM_C-ISR_Réunion #27
  - Proportional calculation methods for different ownership structures

- **Investment Manager Best Practices**
  - Rothschild's sustainable investment methodology (especially for thresholds)
  - Look-through approach for fund structures

## Regulatory Notes

- For **Article 8 funds**, a substantial proportion of sustainable investments (>50%) strengthens the claim
- For **Article 9 funds**, a predominant focus on sustainable investments (typically >80%) is required
- EU Taxonomy alignment percentages are distinct from but related to SFDR sustainable investment percentages
- The calculation methodology follows ASPIM's guidance on applying proportionality based on ownership stake