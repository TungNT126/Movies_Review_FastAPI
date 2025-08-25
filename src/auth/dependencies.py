from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import HTTPException, Request, status

from src.auth.utils import decode_token


class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds =  await super().__call__(request)  
        token = creds.credentials
        token_data = decode_token(token)

        # Kiểm tra token có valid không
        if not self.token_valid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token!")
        
        # Kiểm tra là access token hay refresh token
        if token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide access token!")
        

        return creds
    
    def token_valid(self, token: str):
        token_data = decode_token(token)

        return True if token_data is not None else False