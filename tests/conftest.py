import os

import dotenv
import pytest


@pytest.fixture(autouse=True)
def get_env():
    dotenv.load_dotenv()

@pytest.fixture()
def get_app_url():
    return os.getenv('API_URL')
