# FastAPI Blog API

A simple FastAPI backend project with user registration, JWT authentication, password hashing, and blog management.

## Features
- User creation & login
- JWT authentication
- OAuth2 password flow
- Blog creation (protected routes)
- SQLAlchemy models
- Pydantic schemas

## Run Project

pip install -r requirements.txt

uvicorn Blog.main:app --reload
