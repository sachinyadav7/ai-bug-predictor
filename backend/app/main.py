from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.routes import predict, batch, health, dashboard
from app.auth.routes import router as auth_router
from app.core.model import model_manager
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load model
    print("Loading model...")
    # In a real scenario, we might want to lazy load or handle failures gracefully
    try:
        model_manager.load_model()
    except Exception as e:
        print(f"Warning: Could not load model at startup: {e}")
    yield
    # Shutdown: Cleanup
    print("Shutting down...")

app = FastAPI(
    title="Bug Prediction API",
    description="AI-powered code bug prediction service",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(predict.router, prefix="/api/v1", tags=["Prediction"])
app.include_router(batch.router, prefix="/api/v1", tags=["Batch"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])

@app.get("/")
async def root():
    return {
        "service": "Bug Prediction API",
        "version": "1.0.0",
        "status": "running"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
