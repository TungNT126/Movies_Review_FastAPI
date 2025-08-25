from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from src.auth.schemas import UserBase, UserCreateModel, UserSignUp
from src.auth.service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.utils import verify_passwd
from src.db.main import get_session

from .utils import create_token
from datetime import timedelta

REFRESH_TOKEN_EXP = 2

user_service = UserService()
user_router = APIRouter()

@user_router.post("/signin",response_model=UserBase)
async def sign_in(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exist = await user_service.check_exist(email, session)
    
    if user_exist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email has existed!")
    else: 
        new_user = await user_service.create_user(user_data, session)
    return new_user
        

@user_router.post("/signup")
async def sign_up(login_data:UserSignUp, session: AsyncSession = Depends(get_session)):
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
        

    @user_router.get("/me")
    async def get_current_user(user = Depends(get_current_user)):
        return user

 
