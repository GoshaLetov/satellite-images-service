import uvicorn

from fastapi import FastAPI
from src import planet
from src.config import ClassifierConfig


def main() -> FastAPI:
    app = FastAPI()
    config = ClassifierConfig.from_yaml(path='src/config.yaml')

    container = planet.Container()
    container.config.from_dict(options=config)
    container.wire(modules=[planet.routes])

    app.include_router(router=planet.router)

    return app


if __name__ == '__main__':
    uvicorn.run(main())
