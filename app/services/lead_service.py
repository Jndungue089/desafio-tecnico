from typing import Optional

from bson import ObjectId

from app.db.mongodb import get_database
from app.schemas.lead import LeadCreate, LeadResponse
from app.services.external_api import fetch_birth_date

COLLECTION_NAME = "leads"


def _get_collection():
    return get_database()[COLLECTION_NAME]


async def create_lead(lead_data: LeadCreate) -> LeadResponse:
    birth_date = await fetch_birth_date()

    document = {
        "name": lead_data.name,
        "email": lead_data.email,
        "phone": lead_data.phone,
        "birth_date": birth_date,
    }

    collection = _get_collection()
    result = await collection.insert_one(document)

    return LeadResponse(
        id=str(result.inserted_id),
        name=document["name"],
        email=document["email"],
        phone=document["phone"],
        birth_date=document["birth_date"],
    )


async def list_leads() -> list[LeadResponse]:
    collection = _get_collection()
    leads = []
    async for doc in collection.find():
        leads.append(
            LeadResponse(
                id=str(doc["_id"]),
                name=doc["name"],
                email=doc["email"],
                phone=doc["phone"],
                birth_date=doc.get("birth_date"),
            )
        )
    return leads


async def get_lead_by_id(lead_id: str) -> Optional[LeadResponse]:
    if not ObjectId.is_valid(lead_id):
        return None

    collection = _get_collection()
    doc = await collection.find_one({"_id": ObjectId(lead_id)})
    if not doc:
        return None

    return LeadResponse(
        id=str(doc["_id"]),
        name=doc["name"],
        email=doc["email"],
        phone=doc["phone"],
        birth_date=doc.get("birth_date"),
    )
