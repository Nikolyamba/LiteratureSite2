import pytest


@pytest.mark.asyncio
async def test_create_genre_by_admin(async_client, override_db_dependency, 
                                     override_current_admin):
    payload = {"genre_name": "Sci-Fi",
        "description": "Science Fiction genre",
        "image": "http://example.com/image.png"}
    
    response = await async_client.post('/api/genres', json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data['genre_name'] == payload['genre_name']
    assert data['description'] == payload['description']
    assert data['image'] == payload['image']

@pytest.mark.asyncio
async def test_create_genre_by_user(async_client, override_db_dependency, 
                                     override_current_user):
    
    payload = {"genre_name": "Sci-Fi",
        "description": "Science Fiction genre",
        "image": "http://example.com/image.png"}
    
    response = await async_client.post('/api/genres', json=payload)
    assert response.status_code == 403

    response_json = response.json()
    assert response_json.get('detail') == 'У вас нет прав доступа'

@pytest.mark.asyncio
async def test_create_genre_failure(async_client, override_db_dependency, 
                                     override_current_admin, fake_genre):
    
    payload = {"genre_name": "Detective"}

    response = await async_client.post('/api/genres', json=payload)
    assert response.status_code == 401

    response_json = response.json()
    assert response_json.get('detail') == 'Такой жанр уже есть'