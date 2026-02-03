import pytest


@pytest.mark.asyncio
async def test_healthcheck(async_client):
    response = await async_client.get('/healthcheck')
    assert response.status_code == 200
    assert response.json() == {'success': True}
