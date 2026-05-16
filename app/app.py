from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield
app = FastAPI(lifespan=lifespan)

text_posts = {
    1: {
        "title": "New Post",
        "content": "Cool test post"
    },
    2: {
        "title": "FastAPI Basics",
        "content": "Learning FastAPI step by step."
    },
    3: {
        "title": "Python Tips",
        "content": "Use list comprehensions for cleaner code."
    },
    4: {
        "title": "DSA Journey",
        "content": "Solved 5 recursion problems today."
    }
}


@app.get("/posts")
def get_all_posts(limit: int = None):

    if limit is not None:
        return list(text_posts.values())[:limit]

    return text_posts


@app.get("/posts/{id}", response_model=list[PostResponse])
def get_post(id: int):

    if id not in text_posts:
        raise HTTPException(
            status_code=404,
            detail="Post Not Found"
        )

    return text_posts[id]


@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate):

    new_post = {
        "title": post.title,
        "content": post.content
    }

    new_id = max(text_posts.keys()) + 1

    text_posts[new_id] = new_post

    return new_post