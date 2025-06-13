# python3 -m venv venv --> create virtual environment
from fastapi import FastAPI
from fastapi.params import Body


app = FastAPI(
     title="API for a social media app",
     description="High quality APIs for a social media app",
     version="1.0.0",
     docs_url="/docs",
     redoc_url="/redoc"
    
)
 
@app.get("/")
async def root():
    return {"message": "I'm trying to build high quality APIs"}  

@app.post("/create")
async def create_post(payLoad: dict = Body(...)): # Accepts a required(...) JSON object from the request body as a Python dictionary named payLoad
    print(payLoad)
    return {"new_post": { "title": payLoad["title"], "content": payLoad["content"]}}