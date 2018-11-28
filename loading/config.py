"""Loads the configuration."""
from os import getenv

from dotenv import load_dotenv

from loading.domain import Config


def load_config():
    """Load the Config object from environment variables."""
    load_dotenv()
    return Config(
        getenv('AWS_ACCESS_KEY_ID'),
        getenv('AWS_SECRET_ACCESS_KEY'),
        getenv('AWS_REGION_NAME')
    )
