import pytest
from pftracker import PersonalFinanceTracker
from pftracker.storage import JsonFileStorage


@pytest.fixture
def storage(tmp_path):
    return JsonFileStorage(tmp_path / "finance.json")


@pytest.fixture
def tracker(storage):
    with PersonalFinanceTracker(storage=storage) as tracker:
        yield tracker
