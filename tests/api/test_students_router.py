import pytest

@pytest.mark.asyncio
async def test_create_student_api(client, clear_db):
    """Тест создания студента через API."""
    response = await client.post("/students/", json={
        "full_name": "Тестовый Юзер",
        "group_number": "99"
    })
    assert response.status_code == 200
    assert response.json()["full_name"] == "Тестовый Юзер"

@pytest.mark.asyncio
async def test_create_duplicate_400(client):
    """Тест создания дубликата студента (ожидается ошибка 400)."""
    payload = {"full_name": "Дубль", "group_number": "1"}
    await client.post("/students/", json=payload)
    response = await client.post("/students/", json=payload)
    assert response.status_code == 400