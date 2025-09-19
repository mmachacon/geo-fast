from typing import Dict, List

from .models import Point


def calculate_bounding_box_and_centroid(
    points: List[Point],
) -> Dict[str, Dict[str, float]]:
    """
    Calculates the bounding box (north, south, east, west) and the centroid
    for a given list of geographical points.

    Args:
        points: A list of Point objects, each with 'lat' and 'lng' attributes.
                The list is guaranteed by Pydantic validation to have at least one point.

    Returns:
        A dictionary containing the bounding box and centroid coordinates.
    """
    # Initialize values with the first point's coordinates.
    first_point = points[0]
    north = south = first_point.lat
    east = west = first_point.lng

    # Initialize sums for centroid calculation.
    sum_lat = 0.0
    sum_lng = 0.0

    for point in points:
        # Scan for north, south, east, west
        north = max(north, point.lat)
        south = min(south, point.lat)
        east = max(east, point.lng)
        west = min(west, point.lng)

        # Accumulate sums for centroid
        sum_lat += point.lat
        sum_lng += point.lng

    # Compute the centroid
    num_points = len(points)
    centroid_lat = sum_lat / num_points
    centroid_lng = sum_lng / num_points

    return {
        "bounds": {"north": north, "south": south, "east": east, "west": west},
        "centroid": {"lat": centroid_lat, "lng": centroid_lng},
    }
