import pytest

@pytest.mark.asyncio
async def test_upload_grades_success(client, csv_factory):
    csv_data = csv_factory(["01.01.2025;101Б;Смирнов;5"])
    files = {'file': ('/app/tests/test_data/test.csv', csv_data, 'text/csv')}
    
    response = await client.post("/upload-grades", files=files)
    assert response.status_code == 200
    assert response.json()["details"]["records_loaded"] == 1

@pytest.mark.asyncio
async def test_upload_invalid_extension(client):
    files = {'file': ('test.txt', 'data', 'text/plain')}
    response = await client.post("/upload-grades", files=files)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_reupload_idempotency(client, csv_factory):
    csv_data = csv_factory(["01.01.2025;101;Смирнов;5"])
    files = {'file': ('test.csv', csv_data, 'text/csv')}
    
    await client.post("/upload-grades", files=files)
    response = await client.post("/upload-grades", files=files)
    
    assert response.status_code == 200
    assert response.json()["details"]["records_loaded"] == 1