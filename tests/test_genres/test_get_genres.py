import uuid
import pytest


@pytest.mark.asyncio
async def test_get_all_genres(async_client, override_db_dependency, fake_genre):
    response = await async_client.get('/api/genres')
    assert response.status_code == 200

    response_json = response.json()
    assert isinstance(response_json, list)

    for item in response_json:
        assert 'genre_name' in item
        assert 'image' in item

    assert len(response_json) == 1

#FIXME: Доделать надо будет этот тест потом
""" @pytest.mark.asyncio
async def test_get_genre_books_success(async_client, override_db_dependency, fake_genre):
    genre_id = fake_genre.id
    response = await async_client.get(f'/api/genres/{genre_id}')
    assert response.status_code == 200

    response_json = response.json()
    assert isinstance(response_json, list) """

@pytest.mark.asyncio
async def test_get_genre_books_undefind(async_client, override_db_dependency):
    genre_id = uuid.uuid4()
    response = await async_client.get(f'/api/genres/{genre_id}')
    assert response.status_code == 404

    response_json = response.json()
    assert response_json.get('detail') == 'Такой жанр не найден'