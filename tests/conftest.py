
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import create_application
from app.core.database import Base, get_db_session
from sqlalchemy.types import TypeDecorator, TEXT
import json


class JsonbText(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return value


# Temporarily replace JSONB with JsonbText for SQLite testing
# This needs to be done before Base.metadata.create_all is called
# A more robust solution might involve conditional model definitions or a custom dialect
for table in Base.metadata.tables.values():
    for column in table.columns:
        if str(column.type) == "JSONB":
            column.type = JsonbText()


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def client():
    test_app = create_application(include_trusted_host_middleware=False)
    Base.metadata.create_all(bind=engine)
    test_app.dependency_overrides[get_db_session] = override_get_db
    with TestClient(test_app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
