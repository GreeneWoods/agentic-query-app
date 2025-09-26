from db import leads_collection
import json
import uuid


async def execute_leads_query(
        query_text: str,
        is_high_priority: bool = None
):
    query_filter = {}
    if is_high_priority is not None:
        query_filter['high_priority'] = is_high_priority

    if query_filter:
        leads = leads_collection.query(
            query_texts=[query_text],
            n_results=10,
            where=query_filter
        )
    else:
        leads = leads_collection.query(
            query_texts=[query_text],
            n_results=10
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
    tags = lead_data.get('tags', [])
    tag = ', '.join(tags) if tags else ''

    lead_data['tech_stack'] = tech_stack
    lead_data['tags'] = tag

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


async def create_or_update_lead(lead_data: dict):
    if await is_high_priority_lead(lead_data):
        lead_data['high_priority'] = True
    else:
        lead_data['high_priority'] = False
    document = await convert_lead_into_document(lead_data)
    lead_id = lead_data.get('id', str(uuid.uuid4()))
    leads_collection.upsert(
        ids=[str(lead_id)],
        documents=[document],
        metadatas=[lead_data]
    )
    return lead_id, document, lead_data


async def delete_lead_record(lead_id: str):
    await leads_collection.delete(ids=[lead_id])
    return True
