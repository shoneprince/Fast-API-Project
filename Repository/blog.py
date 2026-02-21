from sqlalchemy.orm import Session
from .. import Models, Schemas
from fastapi import HTTPException, status

def get_all(db: Session):
    blogs = db.query(Models.Blog).all()
    return blogs
    
def create(request: Schemas.Blog, db:Session):
    new_blog = Models.Blog(
    title=request.title,
    body=request.body,
    user_id=1
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id: int, db: Session):
    blog = db.query(Models.Blog).filter(Models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with the id {id}: Not found'
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return

def update(id: int, request: Schemas.Blog, db:Session):
    blog = db.query(Models.Blog).filter(Models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Blog not found'
        )
    blog.update(request.dict())
    db.commit()
    return {'detail': 'Updated successfully'}

def show(id: int, db: Session):
    blog = db.query(Models.Blog).filter(Models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    return blog


    blog = db.query(Models.Blog).filter(Models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Blog not found'
        )
    blog.update(request.dict())
    db.commit()
    return {'detail': 'Updated successfully'}