import uvicorn

from fastapi import FastAPI
from src import planet
from src.config import ServiceConfig


def create_app(config: ServiceConfig) -> FastAPI:
    container = planet.Container()
    container.config.from_dict(options=config)
    container.wire(modules=[planet.routes])

    app = FastAPI()
    app.include_router(router=planet.router, prefix='/planet', tags=['planet'])

    return app


if __name__ == '__main__':
    config = ServiceConfig.from_yaml(path='src/config.yaml')
    uvicorn.run(create_app(config=config), host=config.host, port=config.port)
