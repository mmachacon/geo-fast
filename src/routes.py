from fastapi import APIRouter, status

from .models import PointsPayload
from .utils import calculate_bounding_box_and_centroid

router = APIRouter()


@router.post("/points", status_code=status.HTTP_200_OK)
async def points(payload: PointsPayload):
    """
    Receives a list of geographical points, validates them, calculates the
    bounding box and centroid, and returns the results.
    """
    # The 'payload' argument is an instance of PointsPayload, already parsed and validated.
    result = calculate_bounding_box_and_centroid(payload.points)
    return {
        "status": "success", 
        "message": f"Received {len(payload.points)} points.",
        "result" : result
    }
