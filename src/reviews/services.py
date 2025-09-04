from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Review
from src.reviews.schemas import ReviewCreateModel


class ReviewService:
    # Lấy toàn bộ review của 1 user theo uid
    async def get_user_reviews(self, user_uid: str, session: AsyncSession) -> List[Review]:
        statement = select(Review).where(Review.user_uid == user_uid).order_by(Review.score)
        result = await session.exec(statement)
        
        return result.all()
    
    # Tạo 1 bài Review mới
    async def create_a_review(self, review_data: ReviewCreateModel, user_uid: str, session: AsyncSession):
        review_data_dict = review_data.model_dump()

        new_review = Review(
            **review_data_dict
        )

        new_review.user_uid = user_uid

        session.add(new_review)
        await session.commit()
        return new_review
    
    