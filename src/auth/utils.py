from datetime import datetime, timedelta
import uuid
from passlib.context import CryptContext

import jwt
from src.config import Config
import logging

passwd_context = CryptContext(schemes=['bcrypt'])
ACCESS_TOKEN_EXPIRY = 3600

def hash_passwd(new_passwd: str):
    hashed_passwd = passwd_context.hash(new_passwd)
    return hashed_passwd

def verify_passwd(verify_passwd: str, hashed_passwd: str) -> bool:
    verify = passwd_context.verify(verify_passwd, hashed_passwd)
    if verify:
        return True
    else: 
        return False

# payload(user, exp, jti, refresh)
def create_token(user_data: dict, expiry: timedelta, refresh: bool = False):
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)

        return None


