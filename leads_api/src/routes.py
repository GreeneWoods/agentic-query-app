from fastapi import APIRouter


leads_router = APIRouter(prefix="api/v1/leads")


@leads_router.get('')
def query_leads():
    return []


@leads_router.post('')
def create_lead():
    return True


@leads_router.put('/{lead_id}')
def update_lead(lead_id: str):
    return True


@leads_router.delete('/{lead_id}')
def delete_lead(lead_id: str):
    return True