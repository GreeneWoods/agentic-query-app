from db import leads_collection
import json
import uuid


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


async def create_lead(lead_data: dict):
    if await is_high_priority_lead(lead_data):
        lead_data['high_priority'] = True
    await extract_filters(lead_data)

    lead_id = str(uuid.uuid4())
    lead_id = await leads_collection.add(lead_data)
    return lead_id


async def is_high_priority_lead(lead_data: dict) -> bool:
    if 'company_size' in lead_data:
        if int(lead_data['company_size']) > 500:
            return True
    if 'job_title' in lead_data:
        high_priority_titles = ['vp', 'director']
        if any(title in lead_data['job_title'].lower() for title in high_priority_titles):
            return True
    return False


async def extract_filters(lead_data: dict):
    tags = lead_data.get('tag', [])
    with open('./services/tags.json', 'r') as f:
        all_tags = json.load(f)

    for tag in tags:
        if tag not in all_tags:
            all_tags.append(tag)
            all_tags.sort(key=lambda x: x.lower())
    with open('./services/tags.json', 'w') as f:
        json.dump(all_tags, f, indent=2)

    tech_stacks = lead_data.get('tech_stack', [])
    with open('./services/tech_stacks.json', 'r') as f:
        all_tech_stacks = json.load(f)

    for tech_stack in tech_stacks:
        if tech_stack not in all_tech_stacks:
            all_tech_stacks.append(tech_stack)
            all_tech_stacks.sort(key=lambda x: x.lower())
    with open('./services/tech_stacks.json', 'w') as f:
        json.dump(all_tech_stacks, f, indent=2)
