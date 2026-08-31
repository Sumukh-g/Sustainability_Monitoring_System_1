import pytest
from src.data_generation import generate_data


@pytest.fixture(scope="session")
def sample_data():
    return generate_data(periods=400, sites=("Test",))
