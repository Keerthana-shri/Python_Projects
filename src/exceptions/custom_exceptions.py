from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

async def custom_validation_exception_handler(request: Request, exc: ValidationError):
    errors = [error['msg'] for error in exc.errors()]
    return JSONResponse(
        status_code=400,
        content={"detail": errors},
    )
