from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .exceptions import NotFoundError, ForbiddenError, ValidationError, UnauthorizedError

def register_error_handlers(app: FastAPI):
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"error": "not found"})

    @app.exception_handler(ForbiddenError)
    async def forbidden_handler(request: Request, exc: ForbiddenError):
        return JSONResponse(status_code=403, content={"error": "forbidden"})

    @app.exception_handler(UnauthorizedError)
    async def unauthorized_handler(request: Request, exc: UnauthorizedError):
        return JSONResponse(status_code=401, content={"error": "unauthorized"})

    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=400, 
            content={"error": "validation failed", "fields": exc.fields}
        )

    @app.exception_handler(RequestValidationError)
    async def pydantic_validation_handler(request: Request, exc: RequestValidationError):
        fields = {}
        for error in exc.errors():
            loc = ".".join([str(l) for l in error["loc"]])
            fields[loc] = error["msg"]
        
        return JSONResponse(
            status_code=400,
            content={"error": "validation failed", "fields": fields}
        )

    from starlette.exceptions import HTTPException as StarletteHTTPException
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            return JSONResponse(status_code=404, content={"error": "not found"})
        if exc.status_code == 401:
            return JSONResponse(status_code=401, content={"error": "unauthorized"})
        if exc.status_code == 403:
            return JSONResponse(status_code=403, content={"error": "forbidden"})
        
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": str(exc.detail)}
        )
