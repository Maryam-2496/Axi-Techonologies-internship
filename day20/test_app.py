import pytest
from app import app, db, limiter


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        limiter.reset()
        yield client
        with app.app_context():
            db.drop_all()


def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    assert response.get_json()["email"] == "testuser@example.com"


def test_register_missing_fields(client):
    response = client.post("/auth/register", json={"email": "bad@example.com"})
    assert response.status_code == 400


def test_register_duplicate_email(client):
    client.post(
        "/auth/register",
        json={
            "name": "First User",
            "email": "dupe@example.com",
            "password": "password123",
        },
    )
    response = client.post(
        "/auth/register",
        json={
            "name": "Second User",
            "email": "dupe@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 400


def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "name": "Login User",
            "email": "loginuser@example.com",
            "password": "password123",
        },
    )
    response = client.post(
        "/auth/login",
        json={"email": "loginuser@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "token" in response.get_json()


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "name": "Login User 2",
            "email": "loginuser2@example.com",
            "password": "password123",
        },
    )
    response = client.post(
        "/auth/login",
        json={"email": "loginuser2@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_xss_name_sanitized(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "<b>Ali</b>",
            "email": "xsstest@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    assert "<b>" not in response.get_json()["name"]


def test_login_rate_limit(client):
    client.post(
        "/auth/register",
        json={
            "name": "Rate Test",
            "email": "ratetest@example.com",
            "password": "password123",
        },
    )
    for _ in range(10):
        client.post(
            "/auth/login",
            json={"email": "ratetest@example.com", "password": "wrongpassword"},
        )
    response = client.post(
        "/auth/login",
        json={"email": "ratetest@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 429

def get_auth_token(client):
    """Helper: register + login a test user, return their JWT token."""
    client.post("/auth/register", json={
        "name": "Order Tester",
        "email": "ordertester@example.com",
        "password": "password123"
    })
    resp = client.post("/auth/login", json={
        "email": "ordertester@example.com",
        "password": "password123"
    })
    return resp.get_json()["token"]


def test_create_order_success(client):
    token = get_auth_token(client)
    resp = client.post("/orders",
        json={"item_name": "Keyboard", "amount": 49.99},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 201
    assert resp.get_json()["item_name"] == "Keyboard"


def test_create_order_missing_fields(client):
    token = get_auth_token(client)
    resp = client.post("/orders",
        json={"item_name": "Keyboard"},  # missing amount
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 400


def test_create_order_requires_auth(client):
    resp = client.post("/orders", json={"item_name": "Keyboard", "amount": 49.99})
    assert resp.status_code == 401


def test_get_orders_success(client):
    token = get_auth_token(client)
    client.post("/orders",
        json={"item_name": "Monitor", "amount": 199.99},
        headers={"Authorization": f"Bearer {token}"}
    )
    resp = client.get("/orders", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert "orders" in resp.get_json()
