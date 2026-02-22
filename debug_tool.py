from pydantic import BaseModel, Field
from langchain_core.tools import tool

class MockArgs(BaseModel):
    query: str = Field(description="Search term")
    limit: int = Field(default=5)

@tool("mock_search", args_schema=MockArgs)
def mock_search(query: str, limit: int = 5):
    """Search logic."""
    return f"{query} {limit}"

print(mock_search.args)
