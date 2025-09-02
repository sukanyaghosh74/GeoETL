import pytest

@pytest.fixture(scope="session")
def test_data_dir():
    return "tests/data"
