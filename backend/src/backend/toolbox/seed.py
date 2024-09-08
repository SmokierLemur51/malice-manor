import random
from typing import List

word_list = [
    'one', 'two', 'coffee', 'lover', 
    'sparkle', 'fart', 'smell', 'smart', 
    'table', 'chair', 'bottle', 'water', 
    'cactus', 'plant', 'wood', 'mug', 
    'car', 'plastic', 'spoon', 'fork', 
    'knife', 'butter', 'bean', 'bake', 
    'cold', 'foam', 'new', 'dream', 'milk', 
    'oat', 'almond', 'spare', 'pumpkin', 
    'watermelon', 'apple', 'orange', 'plum', 
    'blueberry', 'strawberrt', 'grandma', 
    'chai', 'summer', 'breeze', 'sugar', 
    'salt', 'pepper', 'garlic', 'onion', 
    'plank', 'muffin', 'coke', 'box', 'carton', 
    'glass', 'window', 'frame', 'nail', 'fin', 
    'fridge', 'freezer', 'siding', 'support', 
    'beam', 'stair', 'rail', 'pool', 
    'fence', 'machine', 'napkin', 'bag',
    'stem', 'toilet', 'mirror', 'lock', 'door',
    'alarm', 'handle', 'key', 'keypad', 'latch',
    'deadbolt', 'shelf', 'newspaper', 'loyal',
    'under', 'over', 'below', 'before', 'after',
    'during', 'end', 'clock', 'bed', 'blanket',
    'pillow', 'backpack', 'leaf', 'stick',
    'ant', 'beatle', 'mockingbird', 'bluejay', 'cardinal', 
    'potion', 'party', 'jug', 'curl', 'carl', 'snarl',
    'mock', 'mach', 'master', 'monkey', 'mega', 'monster',
    'sticker', 'cozy', 'quart', 'flask', 'gin', 'tornado',
    'standard', 'populate', 'population', 'subset', 'sub',
    'contract', 'pay', 'invoice', 'total', 'price', 'selling',
    'cost', 'margin', 'amount', 'percent', 'profit', 
    'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 
    'fifteen', 'sixteen', 'seventeen', 'eighteen', 'hundred',
    'thousand', 'million', 'galleon', 'sickle', 'knuf',
    'crypt', 'crypto', 'cryptocurrency', 'bitcoin', 'monero',
    'btc', 'xmr', 'python', 'go', 'golang', 'rust', 
    'elixir', 'c', 'c++', 'c#', 'zig', 'carbon', 'cigar',
    'cigarette', 'wart', 'port', 'fire', 'firewall', 'rule',
    'ruleset',
]

def generate_seed_phrase(words: List) -> str:
    """ From the given word list, generate a seed phrase 
        for the user to save for later. 

    :param:
    -words: a list of random words, use the provided or others
    """
    seed = []
    # We choose 50 long for now
    for _ in range(50):
        seed.append(words[random.randint(0, len(words)-1)])
    
    return " ".join(seed)



