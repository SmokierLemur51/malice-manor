import random
from typing import List
import secrets

def pick_random_choices(l: List, count: int) -> List:
    """
    Return random item/items from provided list.

    Parameters:
    l (List): List of items you want to sort through, can be of any type.
    count (int): Number of items you want to return.

    Returns:
    List containing (count parameter) number of items from original list
    """
    output = []
    for i in range(count):
        output.append(random.choice(l))
    return output


def convert_list_string(l: List) -> str:
    return "".join(v for v in l)


def generate_secret_key():
    return secrets.token_urlsafe()
