import uvicorn

from fastapi import FastAPI
from src import planet
from src.config import ServiceConfig


def main() -> FastAPI:
    app = FastAPI()
    config = ServiceConfig.from_yaml(path='src/config.yaml')

    for service in [planet]:
        container = service.Container()
        container.config.from_dict(options=config)
        container.wire(modules=[service.routes])

        app.include_router(router=service.router)

    return app


if __name__ == '__main__':
    uvicorn.run(main())
