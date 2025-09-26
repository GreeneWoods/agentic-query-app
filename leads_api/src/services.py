from db import leads_collection


async def query_leads(
        query_text: str,
        tag: str = None,
        tech_stack: str = None,
        is_high_priority: bool = None
):
    filter = {}
    if tag:
        filter['tag'] = tag
    if tech_stack:
        filter['tech_stack'] = tech_stack
    if is_high_priority is not None:
        filter['high_priority'] = is_high_priority

    if len(filter.keys()) > 1:
        filter = {'$and': [{k: v} for k, v in filter.items()]}

    leads = await leads_collection.query(
        query=query_text,
        n_results=10,
        where=filter
    )
    return leads