
from __future__ import annotations

from pymongo import MongoClient
from pymongo.database import Database

from ml_service.core.config import settings

_client: MongoClient | None = None


def get_db() -> Database:
    global _client
    if _client is None:
        _client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=3000)
    return _client[settings.mongo_db]
