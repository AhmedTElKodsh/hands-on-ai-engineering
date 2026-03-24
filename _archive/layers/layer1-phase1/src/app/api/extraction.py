"""
Extraction API endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.extraction import (
    extract_structured_data,
    ExtractionResult,
    ExtractionRequest,
    ContactInfo,
    ProductInfo,
)

router = APIRouter(prefix="/extract", tags=["extraction"])


@router.post(
    "",
    response_model=ExtractionResult,
    summary="Extract structured data from text",
)
async def extract_data(
    request: ExtractionRequest,
):
    """
    Extract structured data from text using LLM.
    
    - **text**: Text to extract data from
    - **schema_json**: Optional JSON Schema for extraction
    - **instructions**: Additional extraction instructions
    - **max_retries**: Maximum retry attempts (default: 3)
    
    Returns extracted data with confidence score and validation info.
    """
    result = await extract_structured_data(
        text=request.text,
        schema_json=request.schema_json,
        instructions=request.instructions,
        max_retries=request.max_retries,
    )
    
    return result


@router.post(
    "/contact",
    response_model=ExtractionResult,
    summary="Extract contact information",
)
async def extract_contact(
    text: str = Query(..., description="Text containing contact information"),
):
    """
    Extract contact information from text.
    
    Extracts: name, email, phone, address, company, job_title
    """
    result = await extract_structured_data(
        text=text,
        schema=ContactInfo,
        instructions="Extract all available contact information. Be thorough but accurate.",
    )
    
    return result


@router.post(
    "/product",
    response_model=ExtractionResult,
    summary="Extract product information",
)
async def extract_product(
    text: str = Query(..., description="Text containing product information"),
):
    """
    Extract product information from text.
    
    Extracts: product_name, price, description, features, category
    """
    result = await extract_structured_data(
        text=text,
        schema=ProductInfo,
        instructions="Extract product details. For price, convert to USD if necessary.",
    )
    
    return result


@router.post(
    "/custom",
    response_model=ExtractionResult,
    summary="Extract with custom schema",
)
async def extract_custom(
    text: str = Body(..., embed=True, description="Text to extract from"),
    schema: str = Body(..., embed=True, description="JSON Schema as string"),
    instructions: Optional[str] = Body(None, embed=True, description="Instructions"),
):
    """
    Extract data using a custom JSON Schema.
    
    Send schema as a JSON string in the request body.
    """
    try:
        import json
        schema_dict = json.loads(schema)
        # Validate it's a proper schema
        if not isinstance(schema_dict, dict):
            raise ValueError("Schema must be a JSON object")
    except json.JSONDecodeError as e:
        raise HTTPException(400, detail=f"Invalid JSON schema: {e}")
    
    result = await extract_structured_data(
        text=text,
        schema_json=schema,
        instructions=instructions,
    )
    
    return result
