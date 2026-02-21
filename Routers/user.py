from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import Models, Schemas, oauth2
from ..Database import get_db
from ..hashing import Hash
from .. Repository import user

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/', response_model=Schemas.ShowUser)
def create_user(request: Schemas.UserCreate, db: Session = Depends(get_db)):
    return user.create(request, db)

@router.get('/{id}', response_model=Schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)

@router.get('/me', response_model=Schemas.ShowUser)
def get_me(current_user = Depends(oauth2.get_current_user)):
    return current_user

