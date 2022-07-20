import os
import uvicorn
import inspect
import re

from fastapi.routing import APIRoute

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from middlewares import setup_middlewares
from models import setup_database
from routers import auth, security


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = FastAPI()

app.include_router(auth.router, prefix='/auth')
app.include_router(security.router, prefix='/security')


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Absolute Wallet",
        version="1.0",
        description="API ",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "Token": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **'Token &lt;Token&gt;'**"
        }
    }
    api_router = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_router:
        path = getattr(route, "path")
        endpoint = getattr(route, "endpoint")
        methods = [method.lower() for method in getattr(route, "methods")]
        for method in methods:
            if (
                    re.search("utils.verifier_cookie", inspect.getsource(endpoint))
            ):
                openapi_schema["paths"][path][method]["security"] = [
                    {
                        "Token": []
                    }
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.on_event("startup")
async def startup_event():
    setup_database(app)
    setup_middlewares(app)


# @app.on_event("shutdown")
# async def shutdown_event():
#     await app.state.redis.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=5004,
        proxy_headers=True,
        forwarded_allow_ips='*',
        reload=True
    )
