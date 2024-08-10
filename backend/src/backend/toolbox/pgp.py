# https://pgpy.readthedocs.io/en/latest/examples.html
from pgpy.constants import (
    PubKeyAlgorith, 
    KeyFlags,
    HashAlgorithms,
    SymmetricKeyAlgorithm,
    CompressionAlgorithm,    
)

# genearte primary key
key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)

# new key does not have user ID yet, rendering it non usable
uid = pgpy.PGPUID.new(
        'Logan Lee', 
        comment='The Creator', 
        email='logandarrinlee@gmail.com',
)

# need to add the new user id to the key. 
# also need to specify all of our preferences here.
# key.add_uid(uid, )
