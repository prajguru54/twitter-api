from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from .utils import post_request, get_request, put_request, delete_request
from user_service.crud import crud_user
from typing import Dict
import pytest
from user_service.core.errors import ResourceNotFoundException

user_sribastav: Dict[str, str | int | bool] = {
    "email": "sribastav@example.com",
    "is_active": True,
    "is_superuser": False,
    "name": "sribastav",
    "id": 1,
}

global access_token


class TestUserCRUDSuccess:
    access_token = ""

    # @pytest.mark.skip
    def test_create_user_success(self, client: TestClient, db: Session):
        response = post_request(
            client=client,
            url="/users",
            json={
                "name": user_sribastav["name"],
                "email": user_sribastav["email"],
                "password": "password",
            },
        )
        assert response == user_sribastav

    # @pytest.mark.skip
    def test_login(self, client: TestClient, db: Session):
        response = post_request(
            client=client,
            url="/users/token",
            data={"username": user_sribastav["email"], "password": "password"},
        )
        # self.access_token = response["access_token"]
        # FIXME: set access_token to a class variable instead of global
        global access_token
        access_token = response["access_token"]

    # @pytest.mark.skip
    def test_get_all_users_success(self, client: TestClient, db: Session):
        response = get_request(client=client, url="/users")
        assert response == [user_sribastav]

    # @pytest.mark.skip(reason="Getting stuck in alembic downgrade")
    def test_get_user_by_id_success(self, client: TestClient, db: Session):
        user = crud_user.get_by_email(
            db, user_sribastav["email"]  # type:ignore
        )
        assert user
        global access_token
        response = get_request(
            client=client,
            url=f"/users/{user.id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response == user_sribastav

    # @pytest.mark.skip(reason="Getting stuck in alembic downgrade")
    def test_update_user_success(self, client: TestClient, db: Session):
        user = crud_user.get_by_email(
            db, user_sribastav["email"]  # type:ignore
        )  # type:ignore
        assert user

        update_data = {
            "is_superuser": True,
            "name": "updated_sribastav",
        }
        global access_token
        response = put_request(
            client=client,
            url=f"/users/{user.id}",
            payload=update_data,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response == {
            "email": "sribastav@example.com",
            "is_active": True,
            "is_superuser": True,
            "name": "updated_sribastav",
            "id": 1,
        }

    # @pytest.mark.skip(reason="Getting stuck in alembic downgrade")
    def test_delete_user_success(self, client: TestClient, db: Session):
        user = crud_user.get_by_email(
            db, user_sribastav["email"]  # type:ignore
        )
        assert user

        response = delete_request(client=client, url=f"/users/{user.id}")
        assert response

        with pytest.raises(ResourceNotFoundException):
            global access_token
            get_request(
                client=client,
                url=f"/users/{user.id}",
                headers={"Authorization": f"Bearer {access_token}"},
            )
