# tests/test_trend_fetcher.py
import pytest
import json
from skills.skill_trend_research import TrendFetcher

def test_trend_fetcher_exists():
    """Test that the trend fetcher module exists"""
    # This will fail initially since the module doesn't exist
    import skills.skill_trend_research
    assert hasattr(skills.skill_trend_research, 'TrendFetcher')

def test_trend_fetcher_contract():
    """Test that the trend fetcher follows the contract"""
    # Load the contract
    with open('skills/skill_trend_research/contract.json') as f:
        contract = json.load(f)
    
    # This test will fail until we implement the actual class
    fetcher = TrendFetcher()
    
    # Check it has required methods
    assert hasattr(fetcher, 'fetch_trends')
    
    # Check method signature matches contract
    import inspect
    sig = inspect.signature(fetcher.fetch_trends)
    params = list(sig.parameters.keys())
    
    # Check required parameters from contract exist
    required_params = contract['input_schema']['required']
    for param in required_params:
        assert param in params

def test_trend_fetcher_output_structure():
    """Test that output matches the contract schema"""
    # This is the "failing test" - it defines what we expect
    fetcher = TrendFetcher()
    result = fetcher.fetch_trends(platform="youtube")
    
    # Check structure
    assert "trends" in result
    assert isinstance(result["trends"], list)
    
    if result["trends"]:
        trend = result["trends"][0]
        assert "topic" in trend
        assert "volume" in trend
        assert "sentiment" in trend
    
    # This test WILL FAIL initially - that's the point!