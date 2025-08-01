from fastapi import FastAPI, HTTPException
from app.db import engine, Base
from app.models import user  # ✅ Registers model
from app.routes import auth
from app.routes import admin
from fastapi.openapi.utils import get_openapi
from app.routes import song_package 
from app.routes import order
from app.routes import song  
from app.routes import admin_orders
from fastapi.staticfiles import StaticFiles
from app.routes import admin_songs
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .db import BASE_DIR
from app.core.config import settings





# ✅ Create app first
app = FastAPI()

# ✅ Create tables
Base.metadata.create_all(bind=engine)

origins = ["*"]
if settings.ALLOWED_ORIGINS != "*":
    origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Auth routers
app.include_router(auth.router)
app.include_router(admin.router)

# ✅ Song Package routers
app.include_router(song_package.router)  # 👈 song package route

# ✅ Order Routers
app.include_router(order.router)

# ✅ Song Package routers

app.include_router(song.router)

# ✅ Admin routers

app.include_router(admin_orders.router)
app.include_router(admin_songs.router)


# Serve uploaded song files from /media/
# Resolve the directory relative to the backend base so the app works
# regardless of the current working directory.
media_dir = BASE_DIR / "media"
# Allow the directory to be missing during startup (tests may create it later)
app.mount("/media", StaticFiles(directory=str(media_dir), check_dir=False), name="media")







# ✅ Root route
@app.get("/")
def root():
    return {"message": "Welcome to Personalizo.al"}


# Endpoint for authenticated file downloads
@app.get("/download/{file_path:path}", include_in_schema=False)
def download_media(file_path: str):
    path = (BASE_DIR / file_path.lstrip("/")).resolve()
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, filename=path.name)

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
