import re
from hashlib import sha256


def hash_contact_number(number: str):
    """
    Since driver who got ban, may re-register with same number, we store hash of driver mobile number,
    to alert the change of reentry.
    """
    if not number:
        return None
    number = re.sub(r"\D", "", number)
    sha256_hash = sha256(number.encode()).hexdigest()
    return sha256_hash
