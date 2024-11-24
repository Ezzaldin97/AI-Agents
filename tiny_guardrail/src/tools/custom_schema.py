from pydantic import BaseModel, Field

class PIIRemovalInput(BaseModel):
    """Input schema for PII Removal."""
    text: str = Field(..., description="input text.")

class BadWordsRemovalInput(BaseModel):
    """Input schema for PII Removal."""
    text: str = Field(..., description="input text.")