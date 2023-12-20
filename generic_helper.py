import re

def get_str_from_food_dict(food_dict: dict):
    
    """
    Converts a dictionary of food items and quantities into a string.

    Parameters:
        - food_dict (dict): Dictionary containing food items as keys and quantities as values.

    Returns:
        - str: A string representation of the food items and quantities.
    """

    result = ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
    return result


def extract_session_id(session_str: str):
    """
    Extracts the session ID from a string containing a session context.

    Parameters:
        - session_str (str): String containing the session context.

    Returns:
        - str: Extracted session ID.
    """
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string

    return ""
