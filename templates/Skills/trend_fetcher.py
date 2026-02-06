import pytest
from skills import trend_fetcher

def test_trend_data_structure():
    """
    Asserts that the trend_fetcher returns a list of dictionaries
    with the expected keys: 'trend_name', 'trend_value', 'timestamp'.
    """
    data = trend_fetcher.get_trends()  # This should fail initially
    assert isinstance(data, list), "Trend data should be a list"
    assert len(data) > 0, "Trend data should not be empty"

    for trend in data:
        assert isinstance(trend, dict), "Each trend should be a dictionary"
        for key in ['trend_name', 'trend_value', 'timestamp']:
            assert key in trend, f"Missing key in trend: {key}"
