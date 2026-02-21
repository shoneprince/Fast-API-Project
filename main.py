from fastapi import FastAPI, status, Depends
from .import Models
from .Database import engine        
from .Routers import blog, user, Authentication


app = FastAPI()

Models.Base.metadata.create_all(bind=engine)

app.include_router(Authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
