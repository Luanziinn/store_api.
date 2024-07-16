import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/products", json={"name": "Test Product", "description": "A product for testing", "price": 10.99})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"

@pytest.mark.asyncio
async def test_update_product():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create_response = await ac.post("/products", json={"name": "Test Product", "description": "A product for testing", "price": 10.99})
        product_id = create_response.json()["id"]
        
        update_response = await ac.put(f"/products/{product_id}", json={"name": "Updated Product", "description": "Updated description", "price": 20.99})
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Product"

@pytest.mark.asyncio
async def test_get_products_by_price_range():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/products", json={"name": "Cheap Product", "description": "Cheap", "price": 100})
        await ac.post("/products", json={"name": "Expensive Product", "description": "Expensive", "price": 7000})
        
        response = await ac.get("/products", params={"min_price": 5000, "max_price": 8000})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Expensive Product"
