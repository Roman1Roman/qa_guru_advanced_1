import requests
from requests import Response

def test_ping(get_app_url) -> None:
    request: Response = requests.get(f'{get_app_url}/ping')
    response = request.json()

    assert request.status_code == 200
    assert response.get('status') == 'pong'
