"""
Structured extraction service for Week 4.

Extracts structured data from text using LLM with Pydantic validation.
"""

from typing import Optional, Type, List
from datetime import datetime
import json

from pydantic import BaseModel, Field, ValidationError
from fastapi import HTTPException

from app.services.llm.client import create_llm_client
from app.services.llm.provider import LLMResponse, LLMError


# Default extraction schema
class ExtractionResult(BaseModel):
    """Default extraction result schema."""
    
    extracted_data: dict = Field(..., description="Extracted structured data")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    missing_fields: List[str] = Field(default_factory=list, description="Missing required fields")
    validation_errors: List[str] = Field(default_factory=list, description="Validation errors")


class ExtractionRequest(BaseModel):
    """Extraction request schema."""
    
    text: str = Field(..., min_length=1, max_length=50000, description="Text to extract from")
    schema_json: Optional[str] = Field(None, description="JSON Schema for extraction")
    instructions: Optional[str] = Field(None, description="Additional extraction instructions")
    max_retries: int = Field(3, ge=1, le=5, description="Maximum retry attempts")


async def extract_structured_data(
    text: str,
    schema: Optional[Type[BaseModel]] = None,
    schema_json: Optional[str] = None,
    instructions: Optional[str] = None,
    max_retries: int = 3,
) -> ExtractionResult:
    """
    Extract structured data from text using LLM.
    
    Args:
        text: Text to extract data from
        schema: Pydantic model class for validation (optional)
        schema_json: JSON Schema string for extraction (optional)
        instructions: Additional extraction instructions
        max_retries: Maximum retry attempts on parse failure
        
    Returns:
        ExtractionResult with extracted data and metadata
        
    Raises:
        HTTPException: If extraction fails after all retries
    """
    llm = create_llm_client()
    
    # Build extraction prompt
    system_prompt = """You are a precise data extraction assistant. Your task is to extract structured data from text according to the provided schema.

Rules:
1. Only extract information explicitly stated in the text
2. Do not invent or assume information not present
3. Return valid JSON matching the schema exactly
4. If a field cannot be determined, set it to null
5. Be conservative - it's better to return null than incorrect data"""

    if instructions:
        system_prompt += f"\n\nAdditional Instructions:\n{instructions}"

    # Build schema description
    if schema:
        schema_desc = json.dumps(schema.model_json_schema(), indent=2)
    elif schema_json:
        schema_desc = schema_json
    else:
        schema_desc = '{"extracted_data": "object", "confidence": "float 0-1", "missing_fields": "array of strings"}'

    user_prompt = f"""Extract data from the following text according to this schema:

Schema:
{schema_desc}

Text:
{text}

Return ONLY valid JSON. Do not include explanations or markdown."""

    # Attempt extraction with retries
    last_error = None
    for attempt in range(max_retries):
        try:
            # Get LLM response
            response: LLMResponse = await llm.complete(
                prompt=user_prompt,
                system_prompt=system_prompt,
            )
            
            # Parse JSON response
            try:
                extracted = json.loads(response.content)
            except json.JSONDecodeError as e:
                # Try to extract JSON from response (sometimes LLM adds markdown)
                import re
                json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
                if json_match:
                    extracted = json.loads(json_match.group())
                else:
                    raise ValueError(f"Failed to parse JSON: {e}")
            
            # Validate against schema if provided
            validation_errors = []
            if schema:
                try:
                    schema(**extracted)
                except ValidationError as ve:
                    validation_errors = [str(e) for e in ve.errors()]
                    if attempt < max_retries - 1:
                        # Retry with error feedback
                        user_prompt = f"""Previous extraction had validation errors. Please fix and try again.

Validation Errors:
{chr(10).join(validation_errors)}

Original Text:
{text}

Return corrected JSON."""
                        continue
            
            # Calculate confidence score
            confidence = calculate_confidence(extracted, validation_errors)
            
            # Identify missing fields
            missing_fields = identify_missing_fields(extracted)
            
            return ExtractionResult(
                extracted_data=extracted,
                confidence=confidence,
                missing_fields=missing_fields,
                validation_errors=validation_errors,
            )
            
        except (LLMError, json.JSONDecodeError, ValueError) as e:
            last_error = e
            if attempt < max_retries - 1:
                import asyncio
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    # All retries exhausted
    raise HTTPException(
        status_code=500,
        detail=f"Extraction failed after {max_retries} attempts: {str(last_error)}",
    )


def calculate_confidence(data: dict, validation_errors: List[str]) -> float:
    """
    Calculate confidence score based on data completeness and validation.
    
    Args:
        data: Extracted data
        validation_errors: List of validation errors
        
    Returns:
        Confidence score 0.0-1.0
    """
    if not data:
        return 0.0
    
    # Start with perfect score
    confidence = 1.0
    
    # Penalize for validation errors
    confidence -= len(validation_errors) * 0.1
    
    # Penalize for null values
    total_fields = len(data)
    null_fields = sum(1 for v in data.values() if v is None)
    if total_fields > 0:
        null_penalty = (null_fields / total_fields) * 0.3
        confidence -= null_penalty
    
    # Ensure bounds
    return max(0.0, min(1.0, round(confidence, 2)))


def identify_missing_fields(data: dict) -> List[str]:
    """
    Identify fields that are null or empty.
    
    Args:
        data: Extracted data
        
    Returns:
        List of missing field names
    """
    missing = []
    for key, value in data.items():
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(key)
    return missing


# Example domain-specific schemas
class ContactInfo(BaseModel):
    """Contact information schema."""
    
    name: Optional[str] = Field(None, description="Full name")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    address: Optional[str] = Field(None, description="Physical address")
    company: Optional[str] = Field(None, description="Company name")
    job_title: Optional[str] = Field(None, description="Job title")


class ProductInfo(BaseModel):
    """Product information schema."""
    
    product_name: Optional[str] = Field(None, description="Product name")
    price: Optional[float] = Field(None, description="Price in USD")
    description: Optional[str] = Field(None, description="Product description")
    features: Optional[List[str]] = Field(default_factory=list, description="Product features")
    category: Optional[str] = Field(None, description="Product category")
