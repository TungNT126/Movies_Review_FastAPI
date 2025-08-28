from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from src.auth.schemas import UserBase, UserCreateModel, UserSignUp
from src.auth.service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user
from src.db.redis import add_jti_to_blocklist

from src.auth.utils import verify_passwd
from src.db.main import get_session

from .utils import create_token
from datetime import datetime, timedelta

REFRESH_TOKEN_EXP = 2

user_service = UserService()
user_router = APIRouter()

@user_router.post("/signup",response_model=UserBase)
async def sign_up(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exist = await user_service.check_exist(email, session)
    
    if user_exist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email has existed!")
    else: 
        new_user = await user_service.create_user(user_data, session)
    return new_user
        

@user_router.post("/signin")
async def sign_in(login_data:UserSignUp, session: AsyncSession = Depends(get_session)):
    # Input email & password
    email = login_data.email
    password = login_data.password

    user = await user_service.check_exist(email, session)

    if user is not None:
        password_valid = verify_passwd(password, user.password_hash)
        if password_valid:
            access_token = create_token(
                user_data={
                    "email": user.email,
                    "uid": str(user.uid)
                },
                expiry=None
            )

            refresh_token = create_token(
                user_data={
                    "email": user.email,
                    "uid": str(user.uid)
                },
                expiry=timedelta(days=REFRESH_TOKEN_EXP),
                refresh=True
            )

            return JSONResponse(
                content={
                    "message": "Login Successfully!",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user":{
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password!")
        

# @user_router.get("/me")
# async def get_current_user(user = Depends(get_current_user)):
#     return user

@user_router.get('/refresh_token')
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    # If exp_time > time right now => expired!
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_token(user_data=token_details['user'], expiry=None)
        return JSONResponse(content={
            "access_token": new_access_token
        })
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")


@user_router.get('/me')
async def get_current_user(user = Depends(get_current_user)):
    return user


@user_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']

    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={
            "message":"Logged out successfully!"
        },
        status_code=status.HTTP_200_OK
    )


