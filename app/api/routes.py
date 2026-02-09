from fastapi import APIRouter, HTTPException

from app.schemas.lead import LeadCreate, LeadResponse
from app.services.lead_service import create_lead, list_leads, get_lead_by_id

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("", response_model=LeadResponse, status_code=201)
async def create_lead_endpoint(lead: LeadCreate):
    """Create a new lead. The birth_date is fetched from an external API."""
    return await create_lead(lead)


@router.get("", response_model=list[LeadResponse])
async def list_leads_endpoint():
    """List all leads."""
    return await list_leads()


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead_endpoint(lead_id: str):
    """Get a lead by its ID."""
    lead = await get_lead_by_id(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead
