"""Registration schemas for account-related operations."""

from typing import Any

from pydantic import BaseModel, EmailStr, Field

from src.apps.accounts.models.users import UserTypeOptions


class UserValidatedDataSchema(BaseModel):
    """Schema for validated user data during registration."""

    user_type: UserTypeOptions = Field(..., description="Type of the user (Candidate or Employer)")

    # User information fields
    email: EmailStr = Field(..., description="User's validated email address")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    phone_number: str | None = Field(None, description="User's phone number (optional)")
    password: str = Field(..., description="User's validated password")

    # Employer-specific fields
    company_name: str | None = Field(None, description="Name of the company (required for employers)")
    company_description: str | None = Field(None, description="Description of the company (optional)")
    company_website: str | None = Field(None, description="Website of the company (optional)")
    company_logo: Any | None = Field(None, description="URL to the company logo (optional)")


class EmployeeInvitationDataSchema(BaseModel):
    """Schema for validated employee invitation data."""

    email: EmailStr = Field(..., description="Employee's validated email address")
    first_name: str = Field(..., description="Employee's first name")
    last_name: str = Field(..., description="Employee's last name")
