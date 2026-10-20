import pytest
from pftracker import PersonalFinanceTracker
from pftracker.storage import JsonFileStorage


@pytest.fixture
def tracker(tmp_path):
    storage = JsonFileStorage(tmp_path / "finance.json")

    with PersonalFinanceTracker(storage=storage) as tracker:
        yield tracker
