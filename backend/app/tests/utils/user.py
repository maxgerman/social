from fastapi.testclient import TestClient

from core.config import settings


def get_superuser_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "email": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f'{settings.API_URL_PREFIX}/auth/login', json=login_data)
    resp = r.json()
    a_token = resp["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def get_user_headers(client: TestClient, email: str, password: str) -> dict[str, str]:
    login_data = {
        'email': email,
        'password': password
    }
    r = client.post(f'{settings.API_URL_PREFIX}/auth/login', json=login_data)
    resp = r.json()
    a_token = resp["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
