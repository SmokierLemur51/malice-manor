import random
import secrets


def generate_vendor_secret():
    # Generate random number to use for iterations of our secret phrase.
    phrase = ""
    for i in range(random.randint(10, 15)):
        phrase.join(secrets.token_urlsafe())
    return phrase

