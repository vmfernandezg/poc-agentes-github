import unittest

from app_ejemplo.login import app


class LoginTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_login_sin_email_devuelve_400(self):
        response = self.client.post("/login", json={"password": "1234"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"ok": False, "mensaje": "El email es obligatorio"},
        )


if __name__ == "__main__":
    unittest.main()
