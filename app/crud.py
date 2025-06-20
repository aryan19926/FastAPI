# python3 -m venv venv --> create virtual environment
# uvicorn main:app --port 8080 --reload


# crud operations

# create -- POST -- to create a resource  /posts
# read -- GET -- to read a resource  /posts/{id} or /posts
# update -- PUT/PATCH -- to update a resource ( put is used to replace the entire resource, patch is used to update a part of the resource) /posts/{id}
# delete -- DELETE -- to delete a resource /posts/{id}



# -- SELECT name AS product_name from public.products WHERE id=1;
# -- SELECT id AS product_id FROM products WHERE id IN (1,2,3);
# -- SELECT * FROM products WHERE id IN (1,2,3);
# -- SELECT * FROM products WHERE name LIKE 'P%';
# -- SELECT * FROM products ORDER BY inventory DESC, price;
# -- SELECT * FROM products ORDER BY inventory DESC, price LIMIT 3;
# -- SELECT * FROM products ORDER BY inventory DESC, price LIMIT 3 OFFSET 2;
# -- INSERT INTO products ( name, price, inventory ) VALUES ( 'keyboard', 25, 36);

# -- INSERT INTO products ( name, price, inventory ) VALUES ( 'keyboard', 25, 36) returning *;
# -- UPDATE products SET name = 'mouse' where id=8;
# -- select * from products;

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi import FastAPI , Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


while True:
    try:
        # cursor_factory=RealDictCursor is used to get the column names as well (not just the values)
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='11825114', cursor_factory=RealDictCursor) 
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)


 
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None


app = FastAPI(
     title="API for a social media app",
     description="High quality APIs for a social media app",
     version="1.0.0",
     docs_url="/docs",
     redoc_url="/redoc"
    
)

# @app.post("/create")
# async def create_post(payLoad: dict = Body(...)): # Accepts a required(...) JSON object from the request body as a Python dictionary named payLoad
#     print(payLoad)
#     return {"new_post": { "title": payLoad["title"], "content": payLoad["content"]}} 

# @app.post("/createpost")
# async def create_post(post: Post):  # post is also a Pydantic model (also have a .dict() method)
#     print(post)
#     print(post.model_dump())  # use model_dump() to convert the Pydantic model to a dictionary
#     # Returning the model directly is implicit—FastAPI does the conversion for you.
#     # return {"new_post": post} 
#     return {"new_post": post.model_dump()}   


# my_posts = [{
#         "id": 1,
#         "title": "this is a test post",
#         "content": "test",
#         "published": True,
#     },
#     {
#         "id": 2,
#         "title": "this is a test post 2",
#         "content": "test 2",
#         "published": True,
#     }]

# def find_index(id: int):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i

@app.get("/")
async def root():
    return {"message": "I'm trying to build high quality APIs"}  

# show all posts
@app.get("/posts")
async def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

# show a single post with the id
@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": post}  

# create a post
@app.post("/posts" , status_code=status.HTTP_201_CREATED)
def create_posts(post: Post): 
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    print(new_post)
    # print(post)
    # my_posts.append(post.model_dump())
    return {"message": "post created successfully", "data": new_post}

# delete a post
# 204 is used to indicate that the request was successful and there is no content to return
@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # in Python, a single-element tuple must have a comma: (int(id),)
    cursor.execute("DELETE FROM posts WHERE id =%s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # my_posts.pop(index)
    # return {"message": "post deleted successfully"} 
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 
# update a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # my_posts[index] = post.model_dump()
    return {"message": "post updated successfully"}

# update a post partially
@app.patch("/posts/{id}")
def patch_post(id: int, post: PostUpdate):
    update_data = post.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
    values = list(update_data.values())
    values.append(id)
    cursor.execute(
        f"UPDATE posts SET {set_clause} WHERE id = %s RETURNING *",
        tuple(values)
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"message": "post updated successfully", "data": updated_post}