from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import Schemas, Database, Models, Token
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(
    tags=['Authentication   ']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(Database.get_db)):
    user = db.query(Models.user).filter(Models.user.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Invalid Credentials')
    if not Hash.verify(user.Password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Incorrect Password')
    
    access_token = Token.create_access_token(data={"sub": user.username})
    return Schemas.Token(access_token=access_token, token_type="bearer")
