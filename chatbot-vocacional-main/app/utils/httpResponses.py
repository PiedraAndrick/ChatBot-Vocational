def create_error_message(message):
    error_message = {
        "status": "Error",
        "data": [],
        "error": {
            "message": message
        }
    }
    return error_message