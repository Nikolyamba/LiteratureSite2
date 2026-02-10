import pytest


@pytest.mark.asyncio
async def test_get_all_books(async_client, override_db_dependency, fake_book):
    response = await async_client.get('/api/books')
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    for item in data:
        assert 'title' in item
        assert 'image' in item

    assert len(data) == 1
