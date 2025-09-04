from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.reviews.schemas import ReviewCreateModel, ReviewUpdateModel
from .services import ReviewService
from src.auth.dependencies import AccessTokenBearer

review_router = APIRouter()
review_service = ReviewService()
access_token_bearer = AccessTokenBearer()

@review_router.get("/")
async def get_user_reviews(user_uid: str, session: AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    reviews = await review_service.get_user_reviews(user_uid, session)
    if reviews is not None:
        return reviews
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Can't find any reviews")
    
@review_router.post("/review_uid")
async def create_a_review(review_data: ReviewCreateModel, user_uid: str, session: AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    new_review = review_service.create_a_review(review_data, user_uid, session)
    
    return new_review


