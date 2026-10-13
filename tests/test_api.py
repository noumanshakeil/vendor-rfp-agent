from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["service"] == "vendor-rfp-agent"


def test_list_and_action():
    r = client.get("/api/requirements")
    assert r.status_code == 200
    assert "requirements" in r.json()

    r2 = client.post("/api/draft_answers", json={"prompt": "smoke test"})
    assert r2.status_code == 200
    body = r2.json()
    assert body["ok"] is True
    assert "result" in body
