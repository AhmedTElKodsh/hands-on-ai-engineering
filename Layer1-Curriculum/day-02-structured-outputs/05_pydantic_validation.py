import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

# ── IMPLEMENTATION ORDER ──────────────────────────────────────────────────────
# TODO 1: Define a Pydantic BaseModel for your extraction target
# TODO 2: Use client.beta.chat.completions.parse() to guarantee structure
# TODO 3: Access the strictly-typed object
# Build in order. Run after each section before moving to the next.

# ── WHAT BROKEN LOOKS LIKE ────────────────────────────────────────────────────
# If PYDANTIC VALIDATION is broken:
#   Error: "pydantic.error_wrappers.ValidationError: 1 validation error"
#   Fix: The LLM returned missing keys. This is rare with `parse`, but usually
#   implies your model schema is too complex or lacks `Optional` typing for nullable fields.

# TODO 1: Define a Pydantic model.
#
# WHY: JSON mode guarantees JSON, but NOT the schema. Pydantic combined with 
# OpenAI's parse() method guarantees both the JSON syntax AND the specific keys/types.
#
# PATTERN:
# class RestaurantReview(BaseModel):
#     name: str
#     rating: int
class RestaurantReview(BaseModel):
    pass

def validate_structured_output():
    # TODO 2: Parse using the beta endpoint.
    #
    # PATTERN:
    # response = client.beta.chat.completions.parse(
    #     model="gpt-4o-mini",
    #     messages=[...],
    #     response_format=RestaurantReview
    # )
    
    # TODO 3: Access the object.
    #
    # WHY: We don't even need json.loads() here. The SDK returns a ready-to-use Python object!
    #
    # EXPECTED: print(review_obj.name)
    pass

if __name__ == "__main__":
    pass
