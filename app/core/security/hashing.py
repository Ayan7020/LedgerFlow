import hashlib

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def verify_token(token: str, token_hash: str) -> bool:
    return hashlib.sha256(token.encode()).hexdigest() == token_hash