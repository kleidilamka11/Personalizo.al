from fastapi import FastAPI
from app.db import engine
from app.models import user  # ✅ Registers model
from app.models.user import Base
from app.routes import auth
from fastapi.openapi.utils import get_openapi


app = FastAPI()  # 🔄 Moved this up first

# 👇 This line actually creates the tables in the database
Base.metadata.create_all(bind=engine)

# 👇 Register routes AFTER creating app
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to Personalizo.al"}



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Personalizo API",
        version="1.0.0",
        description="API for user authentication and personalization features",
        routes=app.routes,
    )

    # 🛠 Ensure components exists
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    # Add Bearer token security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply it globally
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# ✅ Register the custom OpenAPI generator
app.openapi = custom_openapi


