from .. import models, schemas
from ..database import get_db
from ..utils import hash
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    try:
        db.add(new_user)
        db.commit()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email: {user.email} already exists")
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    return user