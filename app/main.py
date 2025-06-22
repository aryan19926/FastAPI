from fastapi import FastAPI , Response, status, HTTPException, Depends
from fastapi.params import Body
from .utils import hash
from . import models, schemas
from .database import engine , get_db
from sqlalchemy.orm import Session
from typing import List
from .routers import users, posts, auth
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
     title="API for a social media app",
     description="High quality APIs for a social media app",
     version="1.0.0",
     docs_url="/docs",
     redoc_url="/redoc"
    
)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "I'm trying to build high quality APIs"}  