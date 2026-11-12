import os
import sqlite3
import tempfile
import pytest
from app import app, init_db
from werkzeug.security import generate_password_hash


@pytest.fixture
def client():
    """Create a test client with a temporary database."""
    db_fd, db_path = tempfile.mkstemp()
    app.config["TESTING"] = True
    app.config["DATABASE"] = db_path
    app.config["SECRET_KEY"] = "test-secret-key"

    with app.app_context():
        init_db()
        yield app.test_client()

    os.close(db_fd)
    os.unlink(db_path)


class TestHomeRoutes:
    """Test public home routes."""

    def test_home_page(self, client):
        """Test home page loads successfully."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Valerii" in response.data or b"Engineer" in response.data

    def test_about_page(self, client):
        """Test about page loads successfully."""
        response = client.get("/about")
        assert response.status_code == 200
        assert b"Alex" in response.data or b"Developer" in response.data

    def test_services_page(self, client):
        """Test services page loads successfully."""
        response = client.get("/services")
        assert response.status_code == 200
        assert b"Construction" in response.data or b"price" in response.data.lower()

    def test_index_page(self, client):
        """Test index page loads successfully."""
        response = client.get("/index")
        assert response.status_code == 200


class TestContactForm:
    """Test contact form functionality."""

    def test_contact_page_get(self, client):
        """Test contact page loads successfully."""
        response = client.get("/contact")
        assert response.status_code == 200

    def test_contact_form_submit_valid(self, client):
        """Test submitting a valid contact form."""
        response = client.post(
            "/contact",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "message": "Test message",
            },
        )
        assert response.status_code == 200
        assert b"John Doe" in response.data or b"success" in response.data.lower()

    def test_contact_form_submit_missing_fields(self, client):
        """Test submitting contact form with missing fields."""
        response = client.post(
            "/contact",
            data={
                "name": "John Doe",
                "email": "",
                "message": "",
            },
        )
        assert response.status_code == 400
        assert b"fill in all fields" in response.data.lower()

    def test_contact_form_empty_name(self, client):
        """Test submitting contact form with empty name."""
        response = client.post(
            "/contact",
            data={
                "name": "",
                "email": "test@example.com",
                "message": "Test message",
            },
        )
        assert response.status_code == 400

    def test_contact_form_whitespace_only(self, client):
        """Test submitting contact form with whitespace-only fields."""
        response = client.post(
            "/contact",
            data={
                "name": "   ",
                "email": "   ",
                "message": "   ",
            },
        )
        assert response.status_code == 400


class TestAdminLogin:
    """Test admin login functionality."""

    def test_login_page_get(self, client):
        """Test login page loads successfully."""
        response = client.get("/admin/login")
        assert response.status_code == 200

    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post(
            "/admin/login",
            data={
                "username": "wrong",
                "password": "wrong",
            },
        )
        assert response.status_code == 401
        assert b"Invalid" in response.data or b"invalid" in response.data.lower()

    def test_login_missing_username(self, client):
        """Test login with missing username."""
        response = client.post(
            "/admin/login",
            data={
                "username": "",
                "password": "password",
            },
        )
        assert response.status_code == 401

    def test_login_missing_password(self, client):
        """Test login with missing password."""
        response = client.post(
            "/admin/login",
            data={
                "username": "admin",
                "password": "",
            },
        )
        assert response.status_code == 401


class TestAdminMessages:
    """Test admin message management functionality."""

    def test_admin_messages_without_login(self, client):
        """Test accessing admin messages without login redirects."""
        response = client.get("/admin/messages", follow_redirects=False)
        assert response.status_code == 302

    def test_delete_message_without_login(self, client):
        """Test deleting message without login redirects."""
        response = client.post("/admin/messages/1/delete", follow_redirects=False)
        assert response.status_code == 302

    def test_edit_message_without_login(self, client):
        """Test editing message without login redirects."""
        response = client.get("/admin/messages/1/edit", follow_redirects=False)
        assert response.status_code == 302


class TestDatabase:
    """Test database operations."""

    def test_database_initialization(self, client):
        """Test that database is properly initialized."""
        connection = sqlite3.connect("messages.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='messages'"
        )
        result = cursor.fetchone()
        connection.close()
        assert result is not None

    def test_message_storage_and_retrieval(self, client):
        """Test storing and retrieving messages from database."""
        client.post(
            "/contact",
            data={
                "name": "Test User",
                "email": "test@example.com",
                "message": "Test message content",
            },
        )

        connection = sqlite3.connect("messages.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM messages WHERE email = ?", ("test@example.com",))
        result = cursor.fetchone()
        connection.close()

        assert result is not None
        assert result["name"] == "Test User"
        assert result["email"] == "test@example.com"
        assert result["message"] == "Test message content"


class TestFlaskConfiguration:
    """Test Flask configuration."""

    def test_app_exists(self):
        """Test that Flask app is created."""
        assert app is not None

    def test_app_is_testing(self, client):
        """Test app testing configuration."""
        assert app.config["TESTING"] is True

    def test_secret_key_configured(self):
        """Test that secret key is configured."""
        assert app.config["SECRET_KEY"] is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
