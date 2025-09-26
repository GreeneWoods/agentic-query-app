from fastapi import APIRouter


leads_router = APIRouter(prefix="api/v1/leads")


@router.get('/')