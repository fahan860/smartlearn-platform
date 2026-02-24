import uvicorn

from config import settings


def run() -> None:
    uvicorn.run("ml_service.main:app", host=settings.host, port=settings.port)


if __name__ == "__main__":
    run()