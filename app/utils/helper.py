import uuid

UNIQUE_ID_TYPE = uuid.UUID

def get_unique_id():
    return uuid.uuid4()