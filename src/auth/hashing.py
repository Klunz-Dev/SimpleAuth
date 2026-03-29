import hmac
import os
import hashlib
from typing import Tuple, Any, Coroutine


async def hash_password(password: str) -> Exception | tuple[str, str] | ValueError:
    try:
        if not password:
            return ValueError('len password < 8')

        salt = os.urandom(16)
        password_bytes = password.encode('utf-8')
        hash_obj = hashlib.sha256()
        hash_obj.update(salt + password_bytes)
        return hash_obj.hexdigest(), salt.hex()
    except Exception as e:
        return e
    
async def verify_password(password: str, save_hash: str, save_salt: str) -> bool:
    try:
        if not password or not save_hash or not save_salt:
            return False
        
        salt = bytes.fromhex(save_salt)
        password_bytes = password.encode('utf-8')

        hash_obj = hashlib.sha256()
        hash_obj.update(salt + password_bytes)
        current_hash = hash_obj.hexdigest()

        return hmac.compare_digest(current_hash, save_hash)

    except:
        return False
