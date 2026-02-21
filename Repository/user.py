from sqlalchemy.orm import Session
from .. import Models, Schemas
from fastapi import HTTPException, status
from .. hashing import Hash

def create(request: Schemas.UserCreate, db: Session):
    new_user = Models.user(
        name=request.name,
        username=request.username,
        Password=Hash.Argon(request.Password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id: int, db: Session):
    user = db.query(Models.user).filter(Models.user.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {id} not found'
        )
    return user