from db import leads_collection
import json
import uuid


async def execute_leads_query(
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


async def convert_lead_into_document(lead_data: dict):
    first_name = lead_data.get('first_name', '')
    last_name = lead_data.get('last_name', '')
    email = lead_data.get('email', '')
    job_title = lead_data.get('job_title', '')
    company = lead_data.get('company', '')
    company_size = lead_data.get('company_size', '')
    industry = lead_data.get('industry', '')
    location = lead_data.get('location', '')
    website = lead_data.get('website', '')
    tech_stacks = lead_data.get('tech_stack', [])
    tech_stack = ', '.join(tech_stacks) if tech_stacks else ''
    lead_source = lead_data.get('lead_source', '')
    last_contacted = lead_data.get('last_contacted', '')
    notes = lead_data.get('notes', '')
    tags = lead_data.get('tag', [])
    tag = ', '.join(tags) if tags else ''

    document_parts = [
        f"First Name: {first_name}",
        f"Last Name: {last_name}",
        f"Email: {email}",
        f"Job Title: {job_title}",
        f"Company: {company}",
        f"Company Size: {company_size}",
        f"Industry: {industry}",
        f"Location: {location}",
        f"Website: {website}",
        f"Tech Stack: {tech_stack}",
        f"Lead Source: {lead_source}",
        f"Last Contacted: {last_contacted}",
        f"Tags: {tag}",
        f"Notes: {notes}"
    ]
    document = "\n".join(document_parts)
    return document


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
    """
    it pains me that this isn't a full db connection, but I wanted to avoid adding
    too much complexity at this time.
    :param lead_data:
    :return:
    """
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


async def create_or_update_lead(lead_data: dict):
    if await is_high_priority_lead(lead_data):
        lead_data['high_priority'] = True
    else:
        lead_data['high_priority'] = False
    await extract_filters(lead_data)
    document = await convert_lead_into_document(lead_data)
    lead_id = lead_data.get('id', str(uuid.uuid4()))
    lead_id = await leads_collection.upsert(
        ids=[lead_id],
        documents=[document],
        metadatas=[lead_data]
    )
    return lead_id, document, lead_data


async def delete_lead_record(lead_id: str):
    await leads_collection.delete(ids=[lead_id])
    return True
