from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.app.api.v1.catalog import router as catalog_router
from backend.app.api.v1.jobs import router as jobs_router
from backend.app.api.v1.assets import router as assets_router
from backend.app.api.v1.deps import get_api_key
from backend.app.core.config import settings

app = FastAPI(
    title="GeoETL API",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(
    catalog_router,
    prefix="/v1",
    dependencies=[Depends(get_api_key)]
)
app.include_router(
    jobs_router,
    prefix="/v1",
    dependencies=[Depends(get_api_key)]
)
app.include_router(
    assets_router,
    prefix="/v1",
    dependencies=[Depends(get_api_key)]
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
