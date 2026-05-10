"""Integration tests for the /hello endpoint."""
from fastapi import status


class TestHelloEndpoint:
    def test_default_returns_hello_world(self, client):
        response = client.get("/api/v1/hello")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Hello, World!"}

    def test_with_name_query_param(self, client):
        response = client.get("/api/v1/hello", params={"name": "Alice"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Hello, Alice!"}

    def test_rejects_empty_name(self, client):
        response = client.get("/api/v1/hello", params={"name": ""})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
