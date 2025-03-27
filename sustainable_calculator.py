"""
Sustainable Real Estate Investment Calculator

This module provides functionality to calculate sustainable investment 
percentages for real estate portfolios according to EU Taxonomy, SFDR,
and industry guidelines from ASPIM and AMF.
"""

from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
import json


@dataclass
class Asset:
    """Represents a real estate asset with sustainability criteria."""
    asset_id: str
    name: str
    market_value: float
    epc_rating: Optional[str] = None
    top_15_percent: bool = False
    nzeb_compliant: bool = False
    renovation_energy_reduction: Optional[float] = None
    renovation_ghg_reduction: Optional[float] = None
    un_sdg_score: Optional[float] = None
    esg_score: Optional[float] = None
    msci_score: Optional[float] = None
    dnsh_compliant: bool = False

    def is_sustainable(self, min_sdg_score: float = 2.5, 
                       min_esg_score: float = 8.0, 
                       min_msci_score: float = 4.0) -> bool:
        """
        Determine if asset qualifies as sustainable based on criteria.
        
        An asset is sustainable if it meets ALL three conditions:
        1. Positive contribution to environmental/social objective
        2. Do No Significant Harm (DNSH) compliance
        3. Good governance practices
        
        Additionally, it must meet at least one technical screening criterion.
        """
        # Check the three main conditions
        positive_contribution = self.un_sdg_score is not None and self.un_sdg_score >= min_sdg_score
        dnsh = self.dnsh_compliant
        good_governance = ((self.esg_score is not None and self.esg_score >= min_esg_score) or 
                          (self.msci_score is not None and self.msci_score >= min_msci_score))
        
        # Check technical screening criteria
        tech_criteria = (
            (self.epc_rating == 'A' or self.top_15_percent) or
            self.nzeb_compliant or
            (self.renovation_energy_reduction is not None and self.renovation_energy_reduction >= 30) or
            (self.renovation_ghg_reduction is not None and self.renovation_ghg_reduction >= 30)
        )
        
        return positive_contribution and dnsh and good_governance and tech_criteria


@dataclass
class SCI:
    """Represents a 100% owned SCI with its assets."""
    sci_id: str
    name: str
    assets: List[Asset]
    ownership_percentage: float = 100.0
    
    def total_value(self) -> float:
        """Calculate the total value of all assets in the SCI."""
        return sum(asset.market_value for asset in self.assets)
    
    def sustainable_value(self, min_sdg_score: float = 2.5, 
                          min_esg_score: float = 8.0, 
                          min_msci_score: float = 4.0) -> float:
        """Calculate the total sustainable value of all assets in the SCI."""
        return sum(asset.market_value for asset in self.assets 
                  if asset.is_sustainable(min_sdg_score, min_esg_score, min_msci_score))
    
    def sustainable_percentage(self, min_sdg_score: float = 2.5, 
                               min_esg_score: float = 8.0, 
                               min_msci_score: float = 4.0) -> float:
        """Calculate the percentage of sustainable assets in the SCI."""
        total = self.total_value()
        if total == 0:
            return 0.0
        return 100.0 * self.sustainable_value(min_sdg_score, min_esg_score, min_msci_score) / total


@dataclass
class Participation:
    """Represents a participation in another investment vehicle."""
    vehicle_id: str
    name: str
    ownership_percentage: float
    total_value: float
    sustainable_percentage: float
    
    def sustainable_value(self) -> float:
        """Calculate the sustainable value of the participation."""
        return self.total_value * (self.sustainable_percentage / 100.0)
    
    def ownership_adjusted_value(self) -> float:
        """Calculate the ownership-adjusted value for uncontrolled participations."""
        return self.total_value * (self.ownership_percentage / 100.0)
    
    def ownership_adjusted_sustainable_value(self) -> float:
        """Calculate the ownership-adjusted sustainable value for uncontrolled participations."""
        return self.ownership_adjusted_value() * (self.sustainable_percentage / 100.0)


@dataclass
class PEFundParticipation:
    """Represents a participation in a private equity fund."""
    fund_id: str
    name: str
    investment_value: float
    estimated_sustainable_percentage: float
    estimation_method: str
    
    def sustainable_value(self) -> float:
        """Calculate the sustainable value of the PE fund participation."""
        return self.investment_value * (self.estimated_sustainable_percentage / 100.0)


class SustainableRealEstateCalculator:
    """Calculator for sustainable real estate investments."""
    
    def __init__(self, 
                 fund_name: str,
                 fund_type: str,
                 reporting_date: str,
                 min_sdg_score: float = 2.5,
                 min_esg_score: float = 8.0,
                 min_msci_score: float = 4.0):
        self.fund_name = fund_name
        self.fund_type = fund_type
        self.reporting_date = reporting_date
        self.min_sdg_score = min_sdg_score
        self.min_esg_score = min_esg_score
        self.min_msci_score = min_msci_score
        
        # Portfolio components
        self.direct_assets: List[Asset] = []
        self.scis: List[SCI] = []
        self.controlled_participations: List[Participation] = []  # >50%
        self.uncontrolled_participations: List[Participation] = []  # 20-50%
        self.minority_stakes: List[Participation] = []  # <20%
        self.pe_fund_participations: List[PEFundParticipation] = []

    def add_direct_asset(self, asset: Asset) -> None:
        """Add a direct asset to the fund."""
        self.direct_assets.append(asset)
    
    def add_sci(self, sci: SCI) -> None:
        """Add a 100% owned SCI to the fund."""
        self.scis.append(sci)
    
    def add_controlled_participation(self, participation: Participation) -> None:
        """Add a controlled participation (>50%) to the fund."""
        if participation.ownership_percentage <= 50:
            raise ValueError("Controlled participations must have >50% ownership")
        self.controlled_participations.append(participation)
    
    def add_uncontrolled_participation(self, participation: Participation) -> None:
        """Add an uncontrolled participation (20-50%) to the fund."""
        if participation.ownership_percentage < 20 or participation.ownership_percentage > 50:
            raise ValueError("Uncontrolled participations must have 20-50% ownership")
        self.uncontrolled_participations.append(participation)
    
    def add_minority_stake(self, participation: Participation) -> None:
        """Add a minority stake (<20%) to the fund."""
        if participation.ownership_percentage >= 20:
            raise ValueError("Minority stakes must have <20% ownership")
        self.minority_stakes.append(participation)
    
    def add_pe_fund_participation(self, pe_fund: PEFundParticipation) -> None:
        """Add a PE fund participation to the fund."""
        self.pe_fund_participations.append(pe_fund)
    
    def calculate_direct_assets(self) -> Tuple[float, float, float]:
        """Calculate total and sustainable values for direct assets."""
        total_value = sum(asset.market_value for asset in self.direct_assets)
        sustainable_value = sum(asset.market_value for asset in self.direct_assets 
                              if asset.is_sustainable(self.min_sdg_score, self.min_esg_score, self.min_msci_score))
        
        sustainable_percentage = 0.0
        if total_value > 0:
            sustainable_percentage = 100.0 * sustainable_value / total_value
            
        return total_value, sustainable_value, sustainable_percentage
    
    def calculate_scis(self) -> Tuple[float, float, float]:
        """Calculate total and sustainable values for 100% owned SCIs."""
        total_value = sum(sci.total_value() for sci in self.scis)
        sustainable_value = sum(sci.sustainable_value(self.min_sdg_score, self.min_esg_score, self.min_msci_score) 
                              for sci in self.scis)
        
        sustainable_percentage = 0.0
        if total_value > 0:
            sustainable_percentage = 100.0 * sustainable_value / total_value
            
        return total_value, sustainable_value, sustainable_percentage
    
    def calculate_controlled_participations(self) -> Tuple[float, float, float]:
        """Calculate total and sustainable values for controlled participations (>50%)."""
        # For controlled participations, we use full consolidation
        total_value = sum(participation.total_value for participation in self.controlled_participations)
        sustainable_value = sum(participation.sustainable_value() for participation in self.controlled_participations)
        
        sustainable_percentage = 0.0
        if total_value > 0:
            sustainable_percentage = 100.0 * sustainable_value / total_value
            
        return total_value, sustainable_value, sustainable_percentage
    
    def calculate_uncontrolled_participations(self) -> Tuple[float, float, float]:
        """Calculate total and sustainable values for uncontrolled participations (20-50%)."""
        # For uncontrolled participations, we apply proportional calculation
        total_value = sum(participation.ownership_adjusted_value() 
                        for participation in self.uncontrolled_participations)
        sustainable_value = sum(participation.ownership_adjusted_sustainable_value() 
                              for participation in self.uncontrolled_participations)
        
        sustainable_percentage = 0.0
        if total_value > 0:
            sustainable_percentage = 100.0 * sustainable_value / total_value
            
        return total_value, sustainable_value, sustainable_percentage
    
    def calculate_minority_stakes(self) -> Tuple[float, float, float]:
        """Calculate total and sustainable values for minority stakes (<20%)."""
        # For minority stakes, we also apply proportional calculation
        total_value = sum(participation.ownership_adjusted_value() 
                        for participation in self.minority_stakes)
        sustainable_value = sum(participation.ownership_adjusted_sustainable_value() 
                              for participation in self.minority_stakes)
        
        sustainable_percentage = 0.0
        if total_value > 0:
            sustainable_percentage = 100.0 * sustainable_value / total_value
            
        return total_value, sustainable_value, sustainable_percentage
    
    def calculate_pe_fund_participations(self) -> Tuple[float, float, float]:
        """Calculate total and sustainable values for PE fund participations."""
        total_value = sum(pe_fund.investment_value for pe_fund in self.pe_fund_participations)
        sustainable_value = sum(pe_fund.sustainable_value() for pe_fund in self.pe_fund_participations)
        
        sustainable_percentage = 0.0
        if total_value > 0:
            sustainable_percentage = 100.0 * sustainable_value / total_value
            
        return total_value, sustainable_value, sustainable_percentage
    
    def calculate_total(self) -> Dict[str, Dict[str, float]]:
        """Calculate the overall sustainability metrics for the fund."""
        direct_assets = self.calculate_direct_assets()
        scis = self.calculate_scis()
        controlled = self.calculate_controlled_participations()
        uncontrolled = self.calculate_uncontrolled_participations()
        minority = self.calculate_minority_stakes()
        pe_funds = self.calculate_pe_fund_participations()
        
        # Calculate fund totals
        total_value = (direct_assets[0] + scis[0] + controlled[0] + 
                      uncontrolled[0] + minority[0] + pe_funds[0])
        
        total_sustainable = (direct_assets[1] + scis[1] + controlled[1] + 
                           uncontrolled[1] + minority[1] + pe_funds[1])
        
        total_sustainable_percentage = 0.0
        if total_value > 0:
            total_sustainable_percentage = 100.0 * total_sustainable / total_value
        
        return {
            "fund_info": {
                "fund_name": self.fund_name,
                "fund_type": self.fund_type, 
                "reporting_date": self.reporting_date
            },
            "direct_assets": {
                "total_value": direct_assets[0],
                "sustainable_value": direct_assets[1],
                "sustainable_percentage": direct_assets[2]
            },
            "scis": {
                "total_value": scis[0],
                "sustainable_value": scis[1],
                "sustainable_percentage": scis[2]
            },
            "controlled_participations": {
                "total_value": controlled[0],
                "sustainable_value": controlled[1],
                "sustainable_percentage": controlled[2]
            },
            "uncontrolled_participations": {
                "total_value": uncontrolled[0],
                "sustainable_value": uncontrolled[1],
                "sustainable_percentage": uncontrolled[2]
            },
            "minority_stakes": {
                "total_value": minority[0],
                "sustainable_value": minority[1],
                "sustainable_percentage": minority[2]
            },
            "pe_fund_participations": {
                "total_value": pe_funds[0],
                "sustainable_value": pe_funds[1],
                "sustainable_percentage": pe_funds[2]
            },
            "fund_total": {
                "total_value": total_value,
                "sustainable_value": total_sustainable,
                "sustainable_percentage": total_sustainable_percentage
            }
        }
    
    def generate_report(self) -> str:
        """Generate a JSON report with the calculation results."""
        return json.dumps(self.calculate_total(), indent=2)