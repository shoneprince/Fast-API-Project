from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import Models, Schemas, oauth2
from ..Database import get_db
from ..Repository import blog 

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)

@router.get('/', response_model=List[Schemas.ShowBlog])
def all(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return blog.get_all(db) 

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: Schemas.BlogBase, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return blog.create(request, db)

@router.get('/{id}',status_code=200, response_model=Schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return blog.show(id, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return blog.destroy(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: Schemas.Blog, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return blog.update(id, request, db)




