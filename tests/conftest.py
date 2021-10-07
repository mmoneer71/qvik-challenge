import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine, SessionLocal, Session
from app.networking import app


@pytest.fixture
def app_client() -> TestClient:
    return TestClient(app)

@pytest.fixture
def clean_state():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


# These are created to be called by pytest only
# The reason is that the above generator can only
# be called within a request context, so these functions will be used
# for service layer unit tests.
# More: https://github.com/tiangolo/fastapi/issues/631


def test_session() -> Session:
    return SessionLocal()


def close_session(db_session: Session):
    db_session.close()
