from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import HTTPException, Request, status

from src.auth.utils import decode_token
from src.db.redis import token_in_blocklist


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds =  await super().__call__(request)  
        token = creds.credentials  # credentials: token
        token_data = decode_token(token)

        # Kiểm tra token có valid không
        if not self.token_valid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail={
                "error":"This token is invalid or has been expired",
                "resolution":"Please get new token"
                }
            )       

        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail={
                "error":"This token is invalid or has been revoked",
                "resolution":"Please get new token"
                }
            )       
           

        self.verify_token_data(token_data)

        return token_data
    
    def token_valid(self, token: str):
        token_data = decode_token(token)

        return True if token_data is not None else False
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in chlid clasess")

        

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        # Kiểm tra là access token hay refresh token
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide access token!")


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        # Kiểm tra là access token hay refresh token
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide refresh token!")

