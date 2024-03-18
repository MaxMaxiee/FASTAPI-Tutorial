from fastapi.testclient import TestClient
from db.database import SessionLocal
from main import app
import unittest
from unittest.mock import MagicMock, patch


client = TestClient(app)


def patch_session_local(func):
    @patch("db.database.SessionLocal")
    def wrapper(self, mock_session_local):
        # Create a MagicMock object that returns a string
        mock_session = MagicMock(return_value="mocked_session")
        mock_session_local.return_value = mock_session
        return func(self, mock_session_local, mock_session)
    return wrapper

class TestUserUnauthenticated(unittest.TestCase):

    @patch_session_local
    def test_create_user(self,  *args):

        payload = {"username": "", "email": "", "password": ""}

        response = client.post("/user", json=payload)
        assert response.status_code == 200

    @patch_session_local
    def test_unauthenticated_get_all_user(self,  *args):
        response = client.get("user/")
        assert response.status_code == 401


class TestUserAuthenticated(unittest.TestCase):

    def setUp(self):
        # Authenticate a user and obtain an access token
        response = client.post('/token',
                               data={"username": "testuser", "password": "testuser"})
        assert response.status_code == 200
        self.access_token = response.json().get("access_token")

    def test_auth_success(self):
        response = client.post('/token',
                            data = {"username": "user", "password": "testpass123"}
                            )
        access_token = response.json().get("access_token")
        assert access_token

    def test_get_all_user(self):
        response = client.get(
            "/user",
            headers = {
                "Authorization": "bearer " + self.access_token
            }
        )
        assert response.status_code == 200

    def test_get_user_by_id(self, *args):
        response = client.get(
            "/user/1",
            headers = {
                "Authorization": "bearer " + self.access_token
            }
        )
        assert response.status_code == 200

    def test_get_user_by_id_not_found(self, *args):
        response = client.get(
            "/user/299",
            headers = {
                "Authorization": "bearer " + self.access_token
            }
        )
        assert response.status_code == 404

    @patch_session_local
    def test_update_user(self,  *args):
        payload = {
            "username": "string",
            "email": "string",
            "password": "string"
        }
        response = client.post(
            "user/2/update",
            json=payload,
            headers = {
                "Authorization": "bearer " + self.access_token
            }
        )
        assert response.status_code == 200

    @patch_session_local
    def test_delete_user(self,  *args):
        response = client.delete(
            "user/2/delete",
            headers = {
                "Authorization": "bearer " + self.access_token
            }
        )
        assert response.status_code == 200


