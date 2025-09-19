from typing import List

from pydantic import BaseModel, ConfigDict, Field


class Point(BaseModel):
    """Represents a single geographical point with latitude and longitude."""

    # Enable strict mode to prevent automatic type coercion (e.g., from string to float).
    # This ensures that 'lat' and 'lng' must be provided as numbers.
    model_config = ConfigDict(strict=True)

    lat: float = Field(
        ...,
        ge=-90.0,
        le=90.0,
        description="Latitude must be between -90 and 90 degrees.",
    )
    lng: float = Field(
        ...,
        ge=-180.0,
        le=180.0,
        description="Longitude must be between -180 and 180 degrees.",
    )


class PointsPayload(BaseModel):
    """Represents the expected JSON payload with a list of points."""

    # The points list must contain at least one item.
    points: List[Point] = Field(..., min_length=1)
