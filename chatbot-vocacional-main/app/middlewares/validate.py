from fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.httpResponses import create_error_message
import re
import json

async def validate_request_body(request: Request, call_next):
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.json()
            if 'text' in body:
                if not isinstance(body['text'], list):
                    return JSONResponse(status_code=400, content=create_error_message("Los datos recibidos tienen un formato incorrecto"))
                for item in body['text']:
                    if not isinstance(item, str):
                        return JSONResponse(status_code=400, content=create_error_message("Todos los items deben ser textos"))
                    if contains_sql_injection(item):
                        return JSONResponse(status_code=400, content=create_error_message("La información recibida contiene valores invalidos"))
        except json.JSONDecodeError:
            return JSONResponse(status_code=400, content=create_error_message("Ocurrio un error inesperado"))
            
    
    response = await call_next(request)
    return response

def contains_sql_injection(text):
    # Simple regex pattern to detect common SQL injection attempts
    pattern = re.compile(r"(SELECT|INSERT|DELETE|UPDATE|DROP|;|--|\*|')", re.IGNORECASE)
    return bool(pattern.search(text))

async def dispatch(request: Request, call_next):
        # Log request
        print(f"Request: {request.method} {request.url}")

        # Get request data
        body = await request.json() if request.method in ['POST', 'PUT'] else {}
        query_params = request.query_params

        # Check for SQL injection patterns
        forbidden_patterns = [
            r"(\%27)|(\')|(\-\-)|(\%23)|(#)",  # SQL meta-characters
            r"(\bSELECT\b)|(\bUNION\b)|(\bINSERT\b)|(\bDELETE\b)|(\bUPDATE\b)|(\bDROP\b)",  # SQL keywords
        ]

        def has_forbidden_pattern(value: str) -> bool:
            for pattern in forbidden_patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    return True
            return False

        # Check body
        for key, value in body.items():
            if isinstance(value, str) and has_forbidden_pattern(value):
                return JSONResponse(status_code=400, content=create_error_message("La información recibida contiene valores invalidos"))

        # Check query params
        for key, value in query_params.items():
            if has_forbidden_pattern(value):
                return JSONResponse(status_code=400, content=create_error_message("La información recibida contiene valores invalidos"))

        response = await call_next(request)
        return response    