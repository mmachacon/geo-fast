import pytest
from fastapi.testclient import TestClient

from main import app
from src.models import Point
from src.utils import calculate_bounding_box_and_centroid

# Create a TestClient instance based on the main FastAPI app
client = TestClient(app)


# =================================================================
# Unit Tests for `utils.py`
# =================================================================


def test_calculate_bounds_and_centroid_single_point():
    """Tests the calculation with a single point."""
    points = [Point(lat=40.7128, lng=-74.0060)]
    result = calculate_bounding_box_and_centroid(points)

    assert result["bounds"]["north"] == 40.7128
    assert result["bounds"]["south"] == 40.7128
    assert result["bounds"]["east"] == -74.0060
    assert result["bounds"]["west"] == -74.0060
    assert result["centroid"]["lat"] == pytest.approx(40.7128)
    assert result["centroid"]["lng"] == pytest.approx(-74.0060)


def test_calculate_bounds_and_centroid_multiple_points():
    """Tests the calculation with a standard set of multiple points."""
    points = [
        Point(lat=40.0, lng=-80.0),  # Southwest
        Point(lat=50.0, lng=-70.0),  # Northeast
    ]
    result = calculate_bounding_box_and_centroid(points)

    assert result["bounds"]["north"] == 50.0
    assert result["bounds"]["south"] == 40.0
    assert result["bounds"]["east"] == -70.0
    assert result["bounds"]["west"] == -80.0
    assert result["centroid"]["lat"] == pytest.approx(45.0)
    assert result["centroid"]["lng"] == pytest.approx(-75.0)


def test_calculate_bounds_and_centroid_crossing_prime_meridian():
    """Tests the calculation with points crossing the prime meridian."""
    points = [Point(lat=10.0, lng=-10.0), Point(lat=20.0, lng=20.0)]
    result = calculate_bounding_box_and_centroid(points)

    assert result["bounds"]["north"] == 20.0
    assert result["bounds"]["south"] == 10.0
    assert result["bounds"]["east"] == 20.0
    assert result["bounds"]["west"] == -10.0
    assert result["centroid"]["lat"] == pytest.approx(15.0)
    assert result["centroid"]["lng"] == pytest.approx(5.0)


# =================================================================
# Integration Tests for the `/points` route
# =================================================================


def test_post_points_success():
    """Tests the happy path with a valid payload."""
    payload = {"points": [{"lat": 10, "lng": 20}, {"lat": 30, "lng": 40}]}
    response = client.post("/points", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert data["message"] == "Received 2 points."
    assert data["result"]["bounds"]["north"] == 30
    assert data["result"]["centroid"]["lat"] == pytest.approx(20)


@pytest.mark.parametrize(
    "payload, expected_error_part",
    [
        (
            {"points": []},
            "List should have at least 1 item",
        ),
        (
            {"points": "not-a-list"},
            "Input should be a valid list",
        ),
        (
            {},
            "Field required",
        ),
        (
            {"points": [{"lat": 91, "lng": 0}]},
            "less than or equal to 90",
        ),
        (
            {"points": [{"lat": 0, "lng": -181}]},
            "greater than or equal to -180",
        ),
        (
            {"points": [{"lat": "40.0", "lng": -70.0}]},
            "Input should be a valid number",
        ),
        (
            {"points": [{"lng": -70.0}]},
            "Field required",
        ),
    ],
)
def test_post_points_bad_request(payload, expected_error_part):
    """
    Tests various invalid payloads that should result in a 400 Bad Request.
    """
    response = client.post("/points", json=payload)
    assert response.status_code == 400
    error_detail = str(response.json()["detail"])
    assert expected_error_part in error_detail

