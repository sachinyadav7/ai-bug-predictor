from fastapi import APIRouter
from app.core.model import model_manager
import torch
import psutil
import os

router = APIRouter()

@router.get("")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model_manager._model is not None,
        "device": str(model_manager._device) if model_manager._device else None,
        "gpu_available": torch.cuda.is_available(),
        "memory_usage": psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB
    }
