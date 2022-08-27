class APIError(Exception):
    status_code: int = 400
    detail: str = 'API error'
