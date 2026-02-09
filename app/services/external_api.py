import httpx

from app.core.config import EXTERNAL_API_URL


async def fetch_birth_date() -> str | None:
    """Fetch birth_date from the external dummyjson API.

    Returns the birthDate string on success, or None if the request fails.
    """
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(EXTERNAL_API_URL)
            response.raise_for_status()
            data = response.json()
            return data.get("birthDate")
    except (httpx.HTTPError, KeyError, Exception):
        return None
