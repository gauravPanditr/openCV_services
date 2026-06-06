import imagehash
from src.config.db import photos

def check_duplicate(phash, claim_id):

    new_hash = imagehash.hex_to_hash(phash)

    docs = photos.find({"claim_id": {"$ne": claim_id}})

    for doc in docs:

        old_hash = imagehash.hex_to_hash(doc["phash"])

        distance = new_hash - old_hash

        if distance <= 5:
            return True, doc["claim_id"]

    return False, None