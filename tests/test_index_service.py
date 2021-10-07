from app.service import get_sample_index


def test_index_service():
    assert get_sample_index().message == "Nothing to see here :eyes:"
