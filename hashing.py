from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class Hash():
    def Argon(Password: str):
            return pwd_context.hash(Password)
    
    def verify(hashed_password, plain_password):
          return pwd_context.verify(plain_password, hashed_password)