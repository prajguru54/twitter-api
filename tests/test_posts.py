import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from user_service.main import app
from user_service.api.dependencies import get_db
from fastapi import  Depends

client = TestClient(app)


# Mocking the Session Local to avoid actual database interactions
@pytest.fixture(scope="module")
def mock_db_session():
    with patch("user_service.api.dependencies.get_db", autospec=True) as mock:
        db_session = MagicMock(spec=Session)
        mock.return_value = db_session
        yield db_session


# Parametrized test cases for happy path, edge cases, and error cases
@pytest.mark.parametrize(
    "keyword, from_date, sort_by, status_code, response_data, test_id",
    [
        # Happy path tests
        (
            "python",
            "2023-01-01",
            "popularity",
            200,
            {
                "articles": [
                    {
                        "title": "Python News",
                        "publishedAt": "2023-01-01T12:00:00Z",
                    }
                ]
            },
            "happy-path-1",
        ),
        (
            "fastapi",
            None,
            None,
            200,
            {
                "articles": [
                    {
                        "title": "FastAPI Updates",
                        "publishedAt": "2023-01-02T12:00:00Z",
                    }
                ]
            },
            "happy-path-2",
        ),
        # Edge cases
        (
            "",
            "2023-01-01",
            "popularity",
            200,
            {"articles": []},
            "edge-case-empty-keyword",
        ),
        (
            "python",
            "2023-01-01",
            "relevancy",
            200,
            {
                "articles": [
                    {
                        "title": "Python Relevancy",
                        "publishedAt": "2023-01-01T12:00:00Z",
                    }
                ]
            },
            "edge-case-diff-sort",
        ),
        # Error cases
        (
            "python",
            "2023-01-01",
            "popularity",
            400,
            {"message": "Bad Request"},
            "error-case-400",
        ),
        (
            "python",
            "2023-01-01",
            "popularity",
            500,
            {"message": "Server Error"},
            "error-case-500",
        ),
    ],
)
def test_search_posts(
    keyword,
    from_date,
    sort_by,
    status_code,
    response_data,
    test_id,
    mock_db_session,
):
    # Arrange
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.json.return_value = response_data
        mock_get.return_value = mock_response

        # Act
        response = client.get(
            f"/?keyword={keyword}&from_date={from_date}&sort_by={sort_by}",
            dependencies=[Depends(lambda: mock_db_session)],
        )

        # Assert
        assert response.status_code == status_code
        if status_code == 200:
            assert response.json() == [
                {
                    "title": article["title"],
                    "date_created": article["publishedAt"],
                }
                for article in response_data["articles"]
            ]
        else:
            assert response.json() == response_data
