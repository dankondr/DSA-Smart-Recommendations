from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from api.endpoints import endpoints as api_router
from core.database import close_database, connect_database
from core.settings import settings

API_NAMESPACE = '/api'

MIDDLEWARES = [
    Middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
]

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    middleware=MIDDLEWARES,
)


@app.on_event('startup')
async def on_startup() -> None:
    await connect_database()


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_database()


app.include_router(api_router, prefix=API_NAMESPACE)
