import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "SmartLearn ML Recommender"
    app_version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8001
    model_path: str = os.getenv("MODEL_PATH", "/app/models/recommender.pkl")


settings = Settings()