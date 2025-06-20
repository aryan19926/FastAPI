from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status , Response, APIRouter
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

# show all posts
@router.get("/", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# show a single post with the id
@router.get("/{id}", response_model=schemas.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post  


# create a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)): 
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    # refresh is used to get the id of the new post, post is not returned by the commit() method
    db.refresh(new_post) 
    return new_post


# delete a post
# 204 is used to indicate that the request was successful and there is no content to return
# the parameter synchronize_session is an argument for SQLAlchemy's delete() and update() methods.
@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 

# update a post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post_query.first())
    return post_query.first()


# update a post partially
# @app.patch("/posts/{id}")
# def patch_post(id: int, post: PostUpdate):
#     update_data = post.model_dump(exclude_unset=True)
#     if not update_data:
#         raise HTTPException(status_code=400, detail="No fields provided for update")
#     set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
#     values = list(update_data.values())
#     values.append(id)
#     cursor.execute(
#         f"UPDATE posts SET {set_clause} WHERE id = %s RETURNING *",
#         tuple(values)
#     )
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#     return {"message": "post updated successfully", "data": updated_post}


@router.patch("/{id}", response_model=schemas.PostResponse)
def patch_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    update_data = post.model_dump(exclude_unset=True)
    post_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(post_query.first())
    return post_query.first()