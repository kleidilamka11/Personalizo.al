from fastapi import FastAPI
from app.db import engine, Base
from app.models import user  # ✅ Registers model
from app.routes import auth
from app.routes import admin
from fastapi.openapi.utils import get_openapi
from app.routes import song_package 
from app.routes import order
from app.routes import song  
from app.routes import admin_orders





# ✅ Create app first
app = FastAPI()

# ✅ Create tables
Base.metadata.create_all(bind=engine)

# ✅ Auth routers
app.include_router(auth.router)
app.include_router(admin.router)

# ✅ Song Package routers
app.include_router(song_package.router)  # 👈 song package route

# ✅ Order Routers
app.include_router(order.router)

# ✅ Song Package routers

app.include_router(song.router)

# ✅ Admin Orders routers

app.include_router(admin_orders.router)





# ✅ Root route
@app.get("/")
def root():
    return {"message": "Welcome to Personalizo.al"}

# ✅ Custom OpenAPI with Bearer auth
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Personalizo API",
        version="1.0.0",
        description="API for user authentication and personalization features",
        routes=app.routes,
    )

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# ✅ Register the custom OpenAPI generator
app.openapi = custom_openapi
