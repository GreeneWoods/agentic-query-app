from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Any, List
import datetime as dt
from pydantic import BaseModel, Field, EmailStr, AnyUrl

from services.leads_services import (
    execute_leads_query,
    create_or_update_lead,
    delete_lead_record
)

leads_router = APIRouter(prefix="/api/v1/leads")


def _parse_bool(value: Any) -> Optional[bool]:
    """Parse a value into a boolean. Accepts bools or common truthy/falsey strings."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    s = str(value).strip().lower()
    if s in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if s in {"0", "false", "f", "no", "n", "off"}:
        return False
    raise HTTPException(status_code=400, detail=f"Invalid boolean value: {value}")


@leads_router.get('')
async def query_leads(
        query: str = Query(..., description="Search query for leads"),
        tag: Optional[str] = Query(None, description="Filter leads by tag"),
        tech_stack: Optional[str] = Query(None, description="Filter leads by tech stack"),
        is_high_priority: Optional[bool] = Query(None, description="Filter high priority leads")
):
    # parse is_high_priority to boolean
    is_high_priority = _parse_bool(is_high_priority)
    leads = await execute_leads_query(
        query_text=query,
        tag=tag,
        tech_stack=tech_stack,
        is_high_priority=is_high_priority
    )

    return leads


class Lead(BaseModel):
    id: int = Field(..., example=87)
    first_name: str = Field(..., example="Gio")
    last_name: str = Field(..., example="Tan")
    email: EmailStr = Field(..., example="gio.tan@silveroakclinic.example")
    job_title: Optional[str] = Field(None, example="VP, Consumer Marketing")
    company: Optional[str] = Field(None, example="SilverOakClinic")
    company_size: Optional[int] = Field(None, example=7000)
    industry: Optional[str] = Field(None, example="Cybersecurity")
    location: Optional[str] = Field(None, example="Singapore, SG")
    website: Optional[AnyUrl] = Field(None, example="https://silveroakclinic.example")
    tech_stack: List[str] = Field(default_factory=list, example=["Snowflake", "Slate"])
    lead_source: Optional[str] = Field(None, example="Community")
    last_contacted: Optional[dt.date] = Field(None, example="2025-09-17")
    notes: Optional[str] = Field(None, example="Exploring LTV-based bidding and fraud mitigation.")
    tags: List[str] = Field(default_factory=list, example=["SKAN", "SDK", "routing", "clean room"])

    def to_dict_form(self):
        return self.model_dump()

@leads_router.post('')
async def create_lead(lead: Lead):
    lead = await create_or_update_lead(lead.to_dict_form())
    return lead


@leads_router.put('/{lead_id}')
async def update_lead(lead_id: str, lead: Lead):
    if str(lead.id) != lead_id:
        raise HTTPException(status_code=400, detail="Lead ID in path and body do not match")
    lead = await create_or_update_lead(lead.to_dict_form())
    return lead


@leads_router.delete('/{lead_id}')
async def delete_lead(lead_id: str):
    success = await delete_lead_record(lead_id)
    return success