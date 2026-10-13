import pytest
@pytest.mark.asyncio
async def test_draft(client):
    await client.post("/api/requirements", json={"text": "SSO via SAML required", "section": "security", "weight": 5})
    r = await client.post("/api/requirements/draft-answers")
    assert r.status_code == 200
    assert r.json()["drafted"] >= 1
