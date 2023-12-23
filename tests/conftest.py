from typing import Dict, Generator
from sqlalchemy_utils import create_database, database_exists, drop_database
import alembic.config
import pytest
from fastapi.testclient import TestClient
from user_service.main import app
from user_service.core.db import session, engine
from dotenv import load_dotenv
import os
from user_service.models import Base

load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def create_tables(client):
    print("setting up create_table")
    print("checking database exists")
    # enable the below lines for local development
    # post development re-enable alembic version of upgrade for testing
    url = os.environ.get("DATABASE_URL", "")
    if database_exists(url):
        print("Database already exists, dropping....")
        drop_database(url)
    print("creating database....")
    create_database(url)
    Base.metadata.create_all(engine)
    # alembic.config.main(argv=["--raiseerr", "upgrade", "head"])

    # yield

    # alembic.config.main(argv=["--raiseerr", "downgrade", "base"])


@pytest.fixture(scope="session")
def db() -> Generator:
    yield session
    session.close()


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
