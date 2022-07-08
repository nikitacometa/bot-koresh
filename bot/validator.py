import base58
import binascii
import hashlib


def is_valid_bitcoin_address(s: str) -> bool:
    base58_decoder = base58.b58decode(s).hex()
    prefix_and_hash = base58_decoder[:len(base58_decoder) - 8]
    checksum = base58_decoder[len(base58_decoder) - 8:]
    addr_hash = prefix_and_hash
    for x in range(1, 3):
        addr_hash = hashlib.sha256(binascii.unhexlify(addr_hash)).hexdigest()
    if checksum == addr_hash[:8]:
        return True
    else:
        return False
