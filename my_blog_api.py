"""Backend FastAPI Server with REST models."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import database_management
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from typing import Optional

origins = ["http://localhost:3000", "http://localhost:8000", "http://localhost:9456"]


class Post(BaseModel):
    id: Optional[int] = None
    author_id: int
    created: datetime
    title: str
    body: str

    class Config:
        orm_mode = True


class Star(BaseModel):
    post_id: int
    user_id: int


class User(BaseModel):
    id: Optional[int] = None
    username: str
    firstName: str
    lastName: str
    email: str
    avatar: str

    class Config:
        orm_mode = True


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


dm = database_management.database_management("blog_database_test2", False)

###########################
######### POSTS ###########
###########################


@app.get("/posts")
def get_posts():
    with Session(dm.engine) as session:
        posts = session.query(database_management.Post).all()
        return posts


@app.post("/posts")
def add_post(post: Post):
    with Session(dm.engine) as session:
        new_post = database_management.Post(
            author_id=post.author_id,
            title=post.title,
            created=post.created,
            body=post.body,
        )
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post


@app.put("/posts")
def put_post(post: Post):
    with Session(dm.engine) as session:
        stm = select(database_management.Post).where(
            database_management.Post.id == post.id
        )
        res = session.execute(stm)
        found_post = res.scalar()
        found_post.title = post.title
        found_post.body = post.body
        session.commit()
        return found_post

@app.delete("/posts/{postId}")
def delete_post(postId: str):
    with Session(dm.engine) as session:
        stm = select(database_management.Post).where(
            database_management.Post.id == postId
        )
        res = session.execute(stm)
        found_post = res.scalar()
        if found_post is not None:
            session.delete(found_post)
            session.commit()
        else:
            raise HTTPException(404, "Post not found")


###########################
######### USERS ###########
###########################


def find_user(username: str, session: Session):
    stm = select(database_management.User).where(
        database_management.User.username == username
    )
    res = session.execute(stm)
    found_user = res.scalar()
    return found_user


@app.get("/users")
def get_users():
    with Session(dm.engine) as session:
        users = session.query(database_management.User).all()
        return users


@app.get("/users/{username}")
def get_user(username: str):
    with Session(dm.engine) as session:
        user = find_user(username=username, session=session)
        return user


@app.post("/users")
def add_user(user: User):
    with Session(dm.engine) as session:
        found_user = find_user(user.username, session)
        if found_user is not None:
            return found_user
        else:
            new_user = database_management.User(
                username=user.username,
                firstName=user.firstName,
                lastName=user.lastName,
                email=user.email,
                avatar=user.avatar,
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user


@app.put("/users")
def put_user(user: User):
    with Session(dm.engine) as session:
        found_user = find_user(user.username, session)
        found_user.email = user.email
        found_user.avatar = user.avatar
        found_user.firstName = user.lastName
        found_user.lastName = user.lastName
        session.commit()


@app.delete("/users/{username}")
def delete_user(username: str):
    with Session(dm.engine) as session:
        found_user = find_user(username, session)  #
        if found_user is not None:
            session.delete(found_user)  #
            session.commit()
        else:
            raise HTTPException(404, "User not found")


###########################
######### STARS ###########
###########################


@app.get("/stars")
def get_stars():
    with Session(dm.engine) as session:
        stars = session.query(database_management.Star).all()
        return stars


@app.post("/stars")
def add_star(star: Star):
    with Session(dm.engine) as session:
        stars = get_stars()
        found_star = next(
            (
                s
                for s in stars
                if s.post_id == star.post_id and s.user_id == star.user_id
            ),
            None,
        )
        if found_star is None:
            new_star = database_management.Star(
                post_id=star.post_id, user_id=star.user_id
            )
            session.add(new_star)
            session.commit()
    return star


@app.delete("/stars/{postId}/{userId}")
def delete_star(postId: int, userId: int):
    with Session(dm.engine) as session:
        stars = get_stars()
        found_star = next(
            (s for s in stars if s.post_id == postId and s.user_id == userId), None
        )
        if found_star is not None:
            session.delete(found_star)
        else:
            raise HTTPException(404, "Star not found")
