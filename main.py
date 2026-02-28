from contextlib import asynccontextmanager
from fastapi import FastAPI
from db import engine
from sqlmodel import SQLModel
from routers.auth import router as auth_router, limiter
from routers.tasks import router as tasks_router

from fastapi.middleware.cors import CORSMiddleware

from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup Logic ---
    # This runs before the application starts taking requests
    SQLModel.metadata.create_all(engine)
    
    yield  # The application runs while stuck here
    
    # --- Shutdown Logic ---
    # This runs after the application finishes handling requests
    # (e.g., close DB connections, clean up resources)
    pass

app = FastAPI(lifespan=lifespan)

# Add the exception handler to the MAIN app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_router)
app.include_router(tasks_router)

origins = [
    "http://localhost:3000",  # e.g. frontend dev server
    "https://myfrontend.com", # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Which domains can access
    allow_credentials=True,       # Allow cookies/headers
    allow_methods=["*"],          # Which HTTP methods
    allow_headers=["*"],          # Which headers
)