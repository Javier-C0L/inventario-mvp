def _create_product(client, sku="TEST-001", quantity=50, min_stock=10):
    response = client.post("/api/v1/products/", json={
        "sku": sku, "name": "Producto de prueba", "quantity": quantity, "min_stock": min_stock,
    })
    assert response.status_code == 201, response.text
    return response.json()


def test_create_product(client):
    product = _create_product(client)
    assert product["quantity"] == 50
    assert product["expiration_status"] == "sin_fecha"


def test_duplicate_sku_rejected(client):
    _create_product(client)
    response = client.post("/api/v1/products/", json={"sku": "TEST-001", "name": "Otro"})
    assert response.status_code == 400


def test_negative_quantity_rejected(client):
    response = client.post("/api/v1/products/", json={"sku": "TEST-002", "name": "X", "quantity": -5})
    assert response.status_code == 422


def test_update_product(client):
    product = _create_product(client)
    response = client.put(f"/api/v1/products/{product['id']}", json={"name": "Renombrado"})
    assert response.status_code == 200
    assert response.json()["name"] == "Renombrado"


def test_delete_product(client):
    product = _create_product(client)
    response = client.delete(f"/api/v1/products/{product['id']}")
    assert response.status_code == 204
    assert client.get(f"/api/v1/products/{product['id']}").status_code == 404


def test_search_and_pagination(client):
    for i in range(15):
        _create_product(client, sku=f"BULK-{i:03d}", quantity=0)
    response = client.get("/api/v1/products/", params={"search": "bulk", "limit": 10})
    body = response.json()
    assert body["total"] == 15
    assert len(body["items"]) == 10
    response = client.get("/api/v1/products/", params={"search": "bulk", "limit": 10, "offset": 10})
    assert len(response.json()["items"]) == 5
