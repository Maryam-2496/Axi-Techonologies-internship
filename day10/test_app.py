import pytest
from app import app, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register_success(client):
    response = client.post("/auth/register", json={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.get_json()["email"] == "testuser@example.com"


def test_register_missing_fields(client):
    response = client.post("/auth/register", json={
        "email": "bad@example.com"
    })
    assert response.status_code == 400


def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "name": "First User",
        "email": "dupe@example.com",
        "password": "password123"
    })
    response = client.post("/auth/register", json={
        "name": "Second User",
        "email": "dupe@example.com",
        "password": "password123"
    })
    assert response.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={
        "name": "Login User",
        "email": "loginuser@example.com",
        "password": "password123"
    })
    response = client.post("/auth/login", json={
        "email": "loginuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "token" in response.get_json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "name": "Login User 2",
        "email": "loginuser2@example.com",
        "password": "password123"
    })
    response = client.post("/auth/login", json={
        "email": "loginuser2@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_xss_name_sanitized(client):
    response = client.post("/auth/register", json={
        "name": "<b>Ali</b>",
        "email": "xsstest@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert "<b>" not in response.get_json()["name"]


def test_login_rate_limit(client):
    client.post("/auth/register", json={
        "name": "Rate Test",
        "email": "ratetest@example.com",
        "password": "password123"
    })
    for _ in range(10):
        client.post("/auth/login", json={
            "email": "ratetest@example.com",
            "password": "wrongpassword"
        })
    response = client.post("/auth/login", json={
        "email": "ratetest@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 429