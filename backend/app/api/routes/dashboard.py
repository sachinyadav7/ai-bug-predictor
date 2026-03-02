from fastapi import APIRouter
from app.core.stats import stats_manager

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats():
    """
    Get real-time dashboard statistics
    """
    return stats_manager.get_dashboard_stats()
