import unittest

from fastapi.testclient import TestClient

from app.main import create_app


class UserModuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(database_url="sqlite:///:memory:")
        self.client = TestClient(self.app)

    def test_register_user_returns_created_user(self) -> None:
        response = self.client.post(
            "/api/v1/users/",
            json={
                "email": "user@example.com",
                "password": "StrongPass123!",
                "full_name": "Test User",
            },
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertEqual(payload["email"], "user@example.com")
        self.assertEqual(payload["full_name"], "Test User")
        self.assertTrue(payload["is_active"])
        self.assertEqual(payload["role"], "member")

    def test_duplicate_email_is_rejected(self) -> None:
        first = self.client.post(
            "/api/v1/users/",
            json={
                "email": "duplicate@example.com",
                "password": "StrongPass123!",
                "full_name": "First User",
            },
        )
        self.assertEqual(first.status_code, 201)

        second = self.client.post(
            "/api/v1/users/",
            json={
                "email": "duplicate@example.com",
                "password": "AnotherPass123!",
                "full_name": "Second User",
            },
        )

        self.assertEqual(second.status_code, 409)
        self.assertIn("already exists", second.text)

    def test_list_users_requires_admin_permission(self) -> None:
        self.client.post(
            "/api/v1/users/",
            json={
                "email": "admin@example.com",
                "password": "StrongPass123!",
                "full_name": "Admin User",
                "role": "admin",
            },
        )

        response = self.client.get(
            "/api/v1/users/",
            headers={"X-User-Role": "member"},
        )

        self.assertEqual(response.status_code, 403)

    def test_list_users_as_admin_returns_users(self) -> None:
        self.client.post(
            "/api/v1/users/",
            json={
                "email": "admin@example.com",
                "password": "StrongPass123!",
                "full_name": "Admin User",
                "role": "admin",
            },
        )

        response = self.client.get(
            "/api/v1/users/",
            headers={"X-User-Role": "admin"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(isinstance(payload, list))
        self.assertGreaterEqual(len(payload), 1)


if __name__ == "__main__":
    unittest.main()
