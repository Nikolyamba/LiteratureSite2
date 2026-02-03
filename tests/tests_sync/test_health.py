from tests.tests_sync.conftest import client


def test_healthcheck():
    response = client.get('/healthcheck')
    assert response.status_code == 200
    assert response.json() == {'success': True}
