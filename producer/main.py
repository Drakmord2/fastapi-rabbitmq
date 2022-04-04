from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import secure

from producer.schemas.main import VersionSchema
from producer.utils.const import ErrorMessage
from producer.controllers import producer

# API instance
app = FastAPI(title="FastAPI", version="1.0.0")

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure.Secure().framework.fastapi(response)
    return response


# Routes
app.include_router(producer.router)

# Index
@app.get("/", tags=["App"], response_model=VersionSchema)
async def api_status():
    """Current API version"""
    return {"name": app.title, "version": app.version}


# Error handler
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": ErrorMessage.GENERIC_ERROR.value, "detail": str(exc)},
    )
