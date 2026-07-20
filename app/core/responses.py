from typing import Any, Dict

def success_response(data: Any = None, message: str = "Success") -> Dict[str, Any]:
    return {"status": "success", "message": message, "data": data}

def error_response(message: str, code: int = 400) -> Dict[str, Any]:
    return {"status": "error", "code": code, "message": message}
