from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer
from src.db.models import Movie
from src.movies.schemas import MovieBase, MovieCreateModel, MovieUpdateModel, MovieReadModel
from src.db.main import get_session
from src.movies.service import MovieService


movie_router = APIRouter()
movie_service = MovieService()
access_token_bearer = AccessTokenBearer()

#Get All Movies
@movie_router.get("/", response_model=List[Movie])
async def get_all_movies(session:AsyncSession = Depends(get_session), user_detail = Depends(access_token_bearer)):
    movies = await movie_service.get_all_movies(session)
    if movies is not None:
        return movies
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found Movie!")

#Search for Movie
@movie_router.get("/{movie_uid}", response_model=MovieReadModel)
async def search_movies_by_uid(movie_uid:str, session:AsyncSession=Depends(get_session), user_detail = Depends(access_token_bearer)):
    movie = await movie_service.search_movies_by_uid(movie_uid,session)
    if movie is not None:
        return movie
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found Movie!")

#Create new Movie
@movie_router.post("/", response_model=Movie)
async def add_movie(movie_data:MovieCreateModel, session:AsyncSession=Depends(get_session), user_detail = Depends(access_token_bearer)):
    new_movie = await movie_service.add_movie(movie_data, session)
    return new_movie

#Update a Movie
@movie_router.patch("/{movie_uid}", response_model=Movie)
async def update_movie(movie_uid: str, update_data: MovieUpdateModel, session:AsyncSession=Depends(get_session), user_detail = Depends(access_token_bearer)):
    movie_to_update = await movie_service.update_movie(movie_uid, update_data, session)
    if movie_to_update is not None:
        return movie_to_update
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found Movie!")
    
#Delete a Movie
@movie_router.delete("/{movie_uid}")
async def delete_movie(movie_uid: str, session:AsyncSession=Depends(get_session), user_detail = Depends(access_token_bearer)):
    deleted_movie = await movie_service.delete_movie(movie_uid,session)
    if deleted_movie is not None:
        return {}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found Movie!")





