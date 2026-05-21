from fastapi import Response


def standard_response(success: bool, data=None, error: str | None = None, status_code: int = 200) -> tuple[dict, int]:
    return {"success": success, "data": data if data is not None else {}, "error": error}, status_code


def success_response(data=None, status_code: int = 200) -> tuple[dict, int]:
    return standard_response(True, data=data, error=None, status_code=status_code)


def error_response(message: str, status_code: int = 400) -> tuple[dict, int]:
    return standard_response(False, data=None, error=message, status_code=status_code)
