from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional


def success(data: Any, message: str = "Success", status_code: int = 200) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "message": message,
            "data": data,
        },
    )


def error(message: str, status_code: int = 400, data: Optional[Dict] = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message,
            "data": data,
        },
    )
