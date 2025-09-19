from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src import routes

# Create the FastAPI application instance.
app = FastAPI(
    title="Geo-Fast API",
    description="API for processing geographical points.",
    version="1.0.0",
)

# Add a custom exception handler to return 400 Bad Request for validation errors.
# This overrides FastAPI's default 422 Unprocessable Entity response.
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles Pydantic validation errors and transforms them into a
    400 Bad Request response, as requested.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        # The `exc.errors()` method provides a detailed list of validation failures.
        content={"detail": exc.errors()},
    )


# Include the router from the routes module.
# This incorporates all the endpoints defined in src/routes.py into the main application.
app.include_router(routes.router)