import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# ── IMPLEMENTATION ORDER ──────────────────────────────────────────────────────
# TODO 1: Load environment variables and initialize the OpenAI client
# TODO 2: Define a sample restaurant review
# TODO 3: Write the system prompt instructing the model to return JSON
# TODO 4: Call the OpenAI API with response_format={"type": "json_object"}
# TODO 5: Parse and print the resulting JSON
# Build in order. Run after each section before moving to the next.

# ── WHAT BROKEN LOOKS LIKE ────────────────────────────────────────────────────
# If JSON MODE is broken:
#   Error: "AttributeError: 'str' object has no attribute 'keys'"
#   Fix: The API returned a JSON string, not a Python dictionary. 
#        Ensure you are using `json.loads(response.choices[0].message.content)`.
#
# If RESPONSE_FORMAT fails:
#   Error: "The response_format parameter requires the word 'json' in the prompt"
#   Fix: Make sure your system prompt explicitly tells the model to output JSON.

def extract_restaurant_info():
    # TODO 1: Load environment variables and initialize the OpenAI client.
    #
    # WHY: The API needs your key to authenticate the request.
    #
    # PATTERN: load_dotenv() \n client = OpenAI()
    # HINT: If you get an AuthenticationError, check your .env file.
    pass

    # TODO 2: Define a sample restaurant review.
    #
    # WHY: We need messy, unstructured text to extract structured data from.
    #
    # EXPECTED: A string containing a review like "The pasta was great but the 
    # service was slow. It cost $50."
    review = """
    We visited 'Luigi's Trattoria' last night. The spaghetti carbonara was absolutely 
    phenomenal, perfectly al dente. However, the waiter forgot our drinks and we had 
    to wait 30 minutes for a table despite having a reservation. Overall price was 
    about $45 per person, which is reasonable for the quality. Rating: 4/5.
    """

    # TODO 3: Write the system prompt instructing the model to return JSON.
    #
    # WHY: The API needs explicit instructions on WHAT to extract and HOW to format it.
    #
    # PATTERN: "Extract: Restaurant name, cuisine, rating, price, pros, cons. Output in JSON."
    # HINT: OpenAI's JSON mode requires the word 'json' in the prompt!
    system_prompt = ""

    # TODO 4: Call the OpenAI API with response_format={"type": "json_object"}.
    #
    # WHY: This setting forces the model to guarantee the output is valid JSON, 
    # preventing parsing errors later.
    #
    # PATTERN: client.chat.completions.create(..., response_format={"type": "json_object"})
    # HINT: Use model "gpt-4o-mini".
    
    # TODO 5: Parse and print the resulting JSON.
    #
    # WHY: The API returns a string that LOOKS like JSON. We need to convert it 
    # to a real Python dictionary so our code can use the fields.
    #
    # PATTERN: data = json.loads(response.choices[0].message.content) \n print(data["name"])
    # EXPECTED: A printed dictionary with keys like 'name', 'cuisine', 'rating'.
    pass

if __name__ == "__main__":
    extract_restaurant_info()
