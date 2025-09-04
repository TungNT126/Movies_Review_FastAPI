from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.movies.routes import movie_router
from src.auth.routes import user_router
from src.reviews.routes import review_router

from src.db.main import init_db, drop_movies_table

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"Server is running...")
    await init_db()
    #await drop_movies_table()
    yield
    print(f"Server has stopped!")

version="v1"


app=FastAPI(
    version=version,
    #lifespan=life_span
)

app.include_router(movie_router, prefix="/api/{version}/movies", tags=["Movies"])
app.include_router(user_router, prefix="/api/{version}/users", tags=['Users']) 
app.include_router(review_router, prefix="/api/{version}/reviews", tags=["Reviews"])