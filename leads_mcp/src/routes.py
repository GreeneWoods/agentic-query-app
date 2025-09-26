from fastmcp import FastMCP
import requests
from config import settings
from typing import Optional

leads_mcp = FastMCP(
    "Lead Query Toolkit",
    "Use this tool to query a vector database of leads.",
    stateless_http=True
)


@leads_mcp.tool()
async def query_leads(query: str, is_high_priority: Optional[bool] = None):
    """Query leads from the vector database based on a search query and optional high priority filter.

    Args:
        query (str): The search query for leads.
        is_high_priority (bool, optional): Filter for high priority leads.

    Returns:
        list: A list of leads matching the search criteria.
    """
    url = f'{settings.api_url}/api/v1/leads'
    params = {'query': query}
    if is_high_priority is not None:
        params['is_high_priority'] = is_high_priority

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()