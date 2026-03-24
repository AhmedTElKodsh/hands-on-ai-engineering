import tiktoken

# ── IMPLEMENTATION ORDER ──────────────────────────────────────────────────────
# TODO 1: Initialize the encoder for 'gpt-4o-mini'
# TODO 2: Write a string of text to encode
# TODO 3: Encode the text into tokens and print the length
# TODO 4: Calculate the estimated cost
# Build in order. Run after each section before moving to the next.

# ── WHAT BROKEN LOOKS LIKE ────────────────────────────────────────────────────
# If TIKTOKEN fails:
#   Error: "Could not automatically map map gpt-4o-mini to a tokeniser"
#   Fix: Ensure you have `tiktoken` updated to a version that supports new models,
#   or explicitly use `tiktoken.get_encoding("o200k_base")`.

def count_tokens():
    # TODO 1: Initialize the encoder.
    #
    # WHY: Different models use different vocabularies. tiktoken needs to know
    # which encoding to use for your specific model.
    #
    # PATTERN: enc = tiktoken.encoding_for_model("gpt-4o-mini")
    pass

    # TODO 2: Use a large string of sample text.
    text = "The quick brown fox jumps over the lazy dog."

    # TODO 3: Encode the text.
    #
    # WHY: LLMs don't read words, they read tokens. A token is roughly 4 characters
    # of English text, but can vary. You pay per token, so counting is crucial.
    #
    # PATTERN: tokens = enc.encode(text) \n num_tokens = len(tokens)
    pass

if __name__ == "__main__":
    count_tokens()
