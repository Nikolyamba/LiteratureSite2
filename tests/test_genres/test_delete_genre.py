import uuid
import pytest


@pytest.mark.asyncio
async def test_delete_genre_success(async_client, fake_genre, override_db_dependency,
                                override_current_admin):
    genre_id = fake_genre.id
    response = await async_client.delete(f'/api/genres/{genre_id}')
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get('msg') == 'Жанр успешно удалён'

@pytest.mark.asyncio
async def test_delete_genre_failure(async_client, fake_genre, override_db_dependency,
                                override_current_user):
    genre_id = fake_genre.id
    response = await async_client.delete(f'/api/genres/{genre_id}')
    assert response.status_code == 403

    response_json = response.json()
    assert response_json.get('detail') == 'У вас нет прав доступа'

@pytest.mark.asyncio
async def test_delete_genre_undefind(async_client, override_db_dependency,
                                override_current_admin):
    genre_id = uuid.uuid4()
    response = await async_client.delete(f'/api/genres/{genre_id}')
    assert response.status_code == 404

    response_json = response.json()
    assert response_json.get('detail') == 'Такой жанр не найден'