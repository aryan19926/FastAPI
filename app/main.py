# python3 -m venv venv --> create virtual environment
# uvicorn main:app --port 8080 --reload


# crud operations

# create -- POST -- to create a resource  /posts
# read -- GET -- to read a resource  /posts/{id} or /posts
# update -- PUT/PATCH -- to update a resource ( put is used to replace the entire resource, patch is used to update a part of the resource) /posts/{id}
# delete -- DELETE -- to delete a resource /posts/{id}


from fastapi import FastAPI , Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

 
class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    rating: Optional[int] = None


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


my_posts = [{
        "id": 1,
        "title": "this is a test post",
        "content": "test",
        "published": True,
    },
    {
        "id": 2,
        "title": "this is a test post 2",
        "content": "test 2",
        "published": True,
    }]

def find_index(id: int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
async def root():
    return {"message": "I'm trying to build high quality APIs"}  

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.get("/posts/{id}")
async def get_post(id: int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": my_posts[index]}  

@app.post("/posts" , status_code=status.HTTP_201_CREATED)
def create_posts(post: Post): 
    print(post)
    my_posts.append(post.model_dump())
    return {"message": "post created successfully"}


@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    my_posts.pop(index)
    # return {"message": "post deleted successfully"} 
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    my_posts[index] = post.model_dump()
    return {"message": "post updated successfully"}

@app.patch("/posts/{id}")
def patch_post(id: int, post: PostUpdate):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    post_data = my_posts[index]
    update_data = post.model_dump(exclude_unset=True)
    post_data.update(update_data)
    my_posts[index] = post_data
    return {"message": "post updated successfully"}