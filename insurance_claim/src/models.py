from pydantic import BaseModel, Field
from typing import List, Optional

class ClaimInfo(BaseModel):
    """
    Input Claim Information schema provided by the Claim Adjuster.
    """
    claim_number: str
    policy_number: str
    claimant_name: str
    date_of_loss: str
    loss_description: str
    estimated_repair_cost: float
    vehicle_details: Optional[str] = None


class PolicyQueries(BaseModel):
    """
    Schema for the list of queries to be used for retrieving relevant policy sections.
    """
    queries: List[str] = Field(
        default_factory=list,
        description="A list of query strings to retrieve relevant policy sections."
    )


class PolicyRecommendation(BaseModel):
    """
    Policy recommendation regarding a given claim.
    """
    policy_section: str = Field(..., description="The policy section or clause that applies.")
    recommendation_summary: str = Field(..., description="A concise summary of coverage determination.")
    deductible: Optional[float] = Field(None, description="The applicable deductible amount.")
    settlement_amount: Optional[float] = Field(None, description="Recommended settlement payout.")


class ClaimDecision(BaseModel):
    """
    Final Claim Decision schema.
    """
    claim_number: str
    covered: bool
    deductible: float
    recommended_payout: float
    notes: Optional[str] = None