import pytest
from skills import example_skill

def test_example_skill_parameters():
    """
    Asserts that the example_skill function accepts the correct parameters:
    - input_data: dict
    - user_context: dict
    """
    input_data = {"sample_key": "sample_value"}
    user_context = {"user": "test"}

    # The function may not exist yet
    result = example_skill.perform_task(input_data, user_context)

    assert result is not None, "Skill should return a result"
    assert isinstance(result, dict), "Result should be a dictionary"
