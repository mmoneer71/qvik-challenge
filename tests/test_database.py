from app.database import get_db_session

def test_get_db_session(clean_state):
    assert get_db_session()
