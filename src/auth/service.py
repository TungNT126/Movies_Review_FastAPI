from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.schemas import UserCreateModel
from src.db.models import User
from src.auth.utils import hash_passwd



class UserService:
    async def get_user_by_email(self, email:str, session:AsyncSession):
        statement = select(User).where(User.email==email)
        result = await session.exec(statement)
        
        return result.first()
        
    async def check_exist(self, email, session: AsyncSession):
        result = await self.get_user_by_email(email, session)
        return result if result is not None else False
        
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        

        user_data_dict = user_data.model_dump()

        new_user = User(
            **user_data_dict
        )

        new_user.password_hash = hash_passwd(user_data_dict['password'])
        new_user.role = "user"
        new_user.is_verified = True

        session.add(new_user)
        await session.commit()
        return new_user


    async def logout(self):
        pass
        

