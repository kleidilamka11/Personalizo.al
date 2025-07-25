from fastapi import FastAPI
from app.db import engine
from app.models import user  # ✅ Registers model
from app.models.user import Base
from app.routes import auth

app = FastAPI()  # 🔄 Moved this up first

# 👇 This line actually creates the tables in the database
Base.metadata.create_all(bind=engine)

# 👇 Register routes AFTER creating app
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to Personalizo.al"}
