"""
Pydantic Models for Business Card Data Validation

This module defines the data schema for extracted business card information.
It ensures type safety and data validation for all API responses.
"""

from pydantic import BaseModel, Field
from typing import Optional


class CardAnalysis(BaseModel):
    """
    Data model representing extracted information from a business card.
    
    All fields are optional as business cards may not contain complete information.
    The completeness_score indicates how much information was available.
    """
    
    full_name: Optional[str] = Field(
        default=None,
        description="Full name of the business card owner"
    )
    job_title: Optional[str] = Field(
        default=None,
        description="Job title or position of the card owner"
    )
    company_name: Optional[str] = Field(
        default=None,
        description="Company or organization name"
    )
    email: Optional[str] = Field(
        default=None,
        description="Email address of the card owner"
    )
    phone_no: Optional[str] = Field(
        default=None,
        description="Phone number of the card owner"
    )
    summary: Optional[str] = Field(
        default=None,
        description="Brief summary or description of the business card"
    )
    completeness_score: float = Field(
        default=0.0,
        ge=0,
        le=100,
        description="Score (0-100) indicating how complete the extracted information is"
    )

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "job_title": "Senior Software Engineer",
                "company_name": "Tech Corp",
                "email": "john.doe@techcorp.com",
                "phone_no": "+1-555-0123",
                "summary": "Senior engineer specializing in cloud infrastructure",
                "completeness_score": 95.0
            }
        }


class BatchResponse(BaseModel):
    """
    Wrapper model for the API response containing extracted card data.
    
    This ensures the response follows the expected structure with a 'card'
    field containing the CardAnalysis data.
    """
    
    card: CardAnalysis = Field(
        ...,
        description="Extracted business card information"
    )

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "card": {
                    "full_name": "John Doe",
                    "job_title": "Senior Software Engineer",
                    "company_name": "Tech Corp",
                    "email": "john.doe@techcorp.com",
                    "phone_no": "+1-555-0123",
                    "summary": "Senior engineer specializing in cloud infrastructure",
                    "completeness_score": 95.0
                }
            }
        }
   
