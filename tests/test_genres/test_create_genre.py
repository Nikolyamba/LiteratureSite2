# from tests.conftest import client
#
#
# def test_create_genre_by_admin(override_current_admin):
#     response = client.post('/genres',
#                            json = {'genre_name': 'Detective'})
#     assert response.status_code == 200
#     data = response.json()
#     assert data['genre_name'] == 'Detective'