import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db import mongodb


@pytest_asyncio.fixture
async def mock_db(monkeypatch):
    """Use mongomock-motor to provide an in-memory MongoDB for tests."""
    from mongomock_motor import AsyncMongoMockClient

    mock_client = AsyncMongoMockClient()
    monkeypatch.setattr(mongodb, "client", mock_client)
    db = mock_client["test_leads_db"]
    monkeypatch.setattr(mongodb, "get_database", lambda: db)

    yield db

    await db.leads.drop()


@pytest_asyncio.fixture
async def client(mock_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_lead(client):
    with patch(
        "app.services.lead_service.fetch_birth_date",
        new_callable=AsyncMock,
        return_value="1998-02-05",
    ):
        response = await client.post(
            "/leads",
            json={
                "name": "João Silva",
                "email": "joao@example.com",
                "phone": "+5511999999999",
            },
        )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "João Silva"
    assert data["email"] == "joao@example.com"
    assert data["phone"] == "+5511999999999"
    assert data["birth_date"] == "1998-02-05"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_lead_external_api_failure(client):
    with patch(
        "app.services.lead_service.fetch_birth_date",
        new_callable=AsyncMock,
        return_value=None,
    ):
        response = await client.post(
            "/leads",
            json={
                "name": "Maria",
                "email": "maria@example.com",
                "phone": "+5511888888888",
            },
        )

    assert response.status_code == 201
    data = response.json()
    assert data["birth_date"] is None


@pytest.mark.asyncio
async def test_list_leads(client):
    with patch(
        "app.services.lead_service.fetch_birth_date",
        new_callable=AsyncMock,
        return_value="1998-02-05",
    ):
        await client.post(
            "/leads",
            json={
                "name": "Lead 1",
                "email": "lead1@example.com",
                "phone": "111",
            },
        )
        await client.post(
            "/leads",
            json={
                "name": "Lead 2",
                "email": "lead2@example.com",
                "phone": "222",
            },
        )

    response = await client.get("/leads")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_lead_by_id(client):
    with patch(
        "app.services.lead_service.fetch_birth_date",
        new_callable=AsyncMock,
        return_value="1998-02-05",
    ):
        create_response = await client.post(
            "/leads",
            json={
                "name": "Test",
                "email": "test@example.com",
                "phone": "123",
            },
        )

    lead_id = create_response.json()["id"]
    response = await client.get(f"/leads/{lead_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test"


@pytest.mark.asyncio
async def test_get_lead_not_found(client):
    response = await client.get("/leads/507f1f77bcf86cd799439011")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_lead_invalid_id(client):
    response = await client.get("/leads/invalid-id")
    assert response.status_code == 404
