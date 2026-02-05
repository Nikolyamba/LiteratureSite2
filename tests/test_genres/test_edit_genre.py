import uuid
import pytest


@pytest.mark.asyncio
async def test_edit_genre_success(async_client, fake_genre, override_db_dependency,
                                override_current_admin):
    genre_id = fake_genre.id
    payload = {"genre_name": "Detective",
        "description": "Something strange"}
    response = await async_client.patch(f'/api/genres/{genre_id}', json=payload)
    assert response.status_code == 200 

    response_json = response.json()
    assert response_json["genre_name"] == payload["genre_name"]
    assert response_json["description"] == payload["description"]
    

@pytest.mark.asyncio
async def test_edit_genre_failure(async_client, fake_genre, override_db_dependency,
                                override_current_user):
    genre_id = fake_genre.id
    payload = {"genre_name": "Detective",
        "description": "Something strange"}
    response = await async_client.patch(f'/api/genres/{genre_id}', json=payload)
    assert response.status_code == 403

    response_json = response.json()
    assert response_json.get('detail') == 'У вас нет прав доступа'


@pytest.mark.asyncio
async def test_edit_genre_undefind(async_client, fake_genre, override_db_dependency,
                                override_current_admin):
    genre_id = uuid.uuid4()
    payload = {"genre_name": "Detective",
        "description": "Something strange"}
    response = await async_client.patch(f'/api/genres/{genre_id}', json=payload)
    assert response.status_code == 404 

    response_json = response.json()
    assert response_json.get('detail') == 'Такой жанр не найден'