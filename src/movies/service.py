from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from src.db.models import Movie
from src.movies.schemas import MovieCreateModel, MovieUpdateModel


class MovieService:
    # Get all movies in db
    async def get_all_movies(self, session: AsyncSession):
        statement = select(Movie).order_by(desc(Movie.released_year))
        result = await session.exec(statement)

        return result.all()
    
    # Get a movie by uid
    async def search_movies_by_uid(self, movie_uid:str, session: AsyncSession):
        statement = select(Movie).where(Movie.uid==movie_uid)
        result = await session.exec(statement)

        return result.first() if result is not None else None

    # Create a new movie
    async def add_movie(self, movie_data:MovieCreateModel, session:AsyncSession):
        movie_data_dict = movie_data.model_dump()
        new_movie = Movie(
            **movie_data_dict
        )

        session.add(new_movie)
        await session.commit()
        return new_movie

    # Update a movie infor
    async def update_movie(self, movie_uid:str, update_data:MovieUpdateModel, session:AsyncSession):
        #Find the targetted movie
        movie_to_update = await self.search_movies_by_uid(movie_uid,session) 

        if movie_to_update is not None:
            # Change from Model to Dictionary
            update_data_dict = update_data.model_dump(exclude_unset=True) # exclude_unset => exclude fields that not been change
            for k,v in update_data_dict.items():
                # Set attributes
                setattr(movie_to_update,k,v) 

            await session.commit()

            return movie_to_update

    # Delete a movie
    async def delete_movie(self, movie_uid:str, session:AsyncSession):
        movie_to_delete = await self.search_movies_by_uid(movie_uid,session)

        if movie_to_delete is not None:
            await session.delete(movie_to_delete)
            await session.commit()

            return True
        else:
            return None
    
