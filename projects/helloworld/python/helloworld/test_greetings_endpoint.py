"""Integration tests for the /greetings endpoint.

These exercise the full stack: HTTP -> route -> service -> SQLAlchemy -> DB.
"""
from fastapi import status


class TestCreateGreeting:
    def test_creates_and_persists(self, client):
        response = client.post(
            "/api/v1/greetings",
            json={"name": "Alice"},
        )
        assert response.status_code == status.HTTP_201_CREATED
        body = response.json()
        assert body["name"] == "Alice"
        assert body["message"] == "Hello, Alice!"
        assert isinstance(body["id"], int)
        assert "created_at" in body

    def test_rejects_missing_name(self, client):
        response = client.post("/api/v1/greetings", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_rejects_empty_name(self, client):
        response = client.post("/api/v1/greetings", json={"name": ""})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestListGreetings:
    def test_empty_list_when_no_data(self, client):
        response = client.get("/api/v1/greetings")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_returns_created_greetings_newest_first(self, client):
        for name in ["Alice", "Bob", "Carol"]:
            client.post("/api/v1/greetings", json={"name": name})

        response = client.get("/api/v1/greetings")
        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert len(body) == 3
        names = [g["name"] for g in body]
        assert names == ["Carol", "Bob", "Alice"]

    def test_respects_limit(self, client):
        for i in range(5):
            client.post("/api/v1/greetings", json={"name": f"User{i}"})

        response = client.get("/api/v1/greetings", params={"limit": 2})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2

    def test_rejects_invalid_limit(self, client):
        response = client.get("/api/v1/greetings", params={"limit": 0})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestHealthEndpoint:
    def test_returns_ok(self, client):
        response = client.get("/api/v1/health")
        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["status"] == "ok"
        assert body["database"] == "ok"
