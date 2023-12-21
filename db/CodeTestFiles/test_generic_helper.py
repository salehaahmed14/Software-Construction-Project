import re
from generic_helper import get_str_from_food_dict, extract_session_id

def test_get_str_from_food_dict():
    # Test Case 1: Empty Dictionary
    empty_food_dict = {}
    result_empty = get_str_from_food_dict(empty_food_dict)
    assert result_empty == ""

    # Test Case 2: Single Element Dictionary
    single_element_dict = {"apple": 2}
    result_single_element = get_str_from_food_dict(single_element_dict)
    assert result_single_element == "2 apple"

    # Test Case 3: Multiple Elements in the Dictionary
    multiple_elements_dict = {"apple": 2, "banana": 3, "orange": 1}
    result_multiple_elements = get_str_from_food_dict(multiple_elements_dict)
    assert result_multiple_elements == "2 apple, 3 banana, 1 orange"

def test_extract_session_id():
    #Test Case 1: Test with a valid session string
    session_str = "/sessions/12345/contexts/some_context"
    result = extract_session_id(session_str)
    assert result == "12345"

    #Test Case 2: Test with a different session string
    session_str_diff = "/sessions/67890/contexts/another_context"
    result_diff = extract_session_id(session_str_diff)
    assert result_diff == "67890"

    #Test Case 3: Test with a session string that doesn't match the pattern
    session_str_invalid = "/some/invalid/path"
    result_invalid = extract_session_id(session_str_invalid)
    assert result_invalid == ""

    #Test Case 4: Test with an empty session string
    session_str_empty = ""
    result_empty = extract_session_id(session_str_empty)
    assert result_empty == ""
