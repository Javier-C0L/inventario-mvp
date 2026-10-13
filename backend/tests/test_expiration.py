from datetime import date, timedelta

from app.services.expiration import expiration_status


def test_expired():
    yesterday = date.today() - timedelta(days=1)
    assert expiration_status(yesterday, 30) == "vencido"


def test_expiring_soon():
    in_10_days = date.today() + timedelta(days=10)
    assert expiration_status(in_10_days, 30) == "proximo_a_vencer"


def test_still_valid():
    in_60_days = date.today() + timedelta(days=60)
    assert expiration_status(in_60_days, 30) == "vigente"


def test_no_date():
    assert expiration_status(None, 30) == "sin_fecha"


def test_warning_days_respected():
    in_40_days = date.today() + timedelta(days=40)
    assert expiration_status(in_40_days, 30) == "vigente"
    assert expiration_status(in_40_days, 45) == "proximo_a_vencer"


def test_settings_update(client):
    response = client.get("/api/v1/settings/")
    assert response.status_code == 200
    response = client.put("/api/v1/settings/", json={"expiration_warning_days": 45})
    assert response.status_code == 200
    assert response.json()["expiration_warning_days"] == 45
    assert client.get("/api/v1/settings/").json()["expiration_warning_days"] == 45


def test_settings_validation(client):
    response = client.put("/api/v1/settings/", json={"expiration_warning_days": 999})
    assert response.status_code == 422


def test_expiration_filter(client):
    today = date.today()
    expiring = today + timedelta(days=10)
    client.post("/api/v1/products/", json={"sku": "EXP-001", "name": "Por vencer", "expiration_date": expiring.isoformat()})
    client.post("/api/v1/products/", json={"sku": "EXP-002", "name": "Vencido", "expiration_date": (today - timedelta(days=1)).isoformat()})
    body = client.get("/api/v1/products/", params={"expiration": "proximo_a_vencer"}).json()
    assert body["total"] == 1
    assert body["items"][0]["sku"] == "EXP-001"
    body = client.get("/api/v1/products/", params={"expiration": "vencido"}).json()
    assert body["total"] == 1
    assert body["items"][0]["sku"] == "EXP-002"
