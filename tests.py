import pytest
from app import app, get_db, init_db


@pytest.fixture
def client():
    """Create a test client backed by an empty messages table."""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key"

    with app.app_context():
        init_db()
        with get_db() as connection:
            connection.execute("TRUNCATE messages, employees RESTART IDENTITY")
        init_db()  # re-seed the default employees
        yield app.test_client()


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
        with get_db() as connection:
            result = connection.execute(
                "SELECT to_regclass('public.messages') AS tbl"
            ).fetchone()
        assert result["tbl"] is not None

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

        with get_db() as connection:
            result = connection.execute(
                "SELECT * FROM messages WHERE email = %s", ("test@example.com",)
            ).fetchone()

        assert result is not None
        assert result["name"] == "Test User"
        assert result["email"] == "test@example.com"
        assert result["message"] == "Test message content"


class TestEmployees:
    """Test employees stored in PostgreSQL."""

    def test_about_lists_seeded_employees(self, client):
        response = client.get("/about")
        assert b"Developer" in response.data
        assert b"Architect" in response.data

    def test_api_get_employees(self, client):
        response = client.get("/api/employees")
        assert response.status_code == 200
        employees = response.get_json()
        assert len(employees) == 5
        assert employees[0]["name"] == "Alex"
        assert employees[0]["salary"] == 3300

    def test_about_has_no_add_employee_form(self, client):
        assert b"add-employee-form" not in client.get("/about").data

    def test_admin_messages_has_add_employee_form(self, client):
        with client.session_transaction() as sess:
            sess["logged_in"] = True
        assert b"add-employee-form" in client.get("/admin/messages").data

    def test_api_add_employee_requires_login(self, client):
        response = client.post(
            "/api/employees",
            json={"name": "Zoe", "age": 27, "position": "Tester", "salary": 3100.5},
        )
        assert response.status_code == 401
        assert len(client.get("/api/employees").get_json()) == 5

    def test_api_add_employee_persists(self, client):
        with client.session_transaction() as sess:
            sess["logged_in"] = True
        response = client.post(
            "/api/employees",
            json={"name": "Zoe", "age": 27, "position": "Tester", "salary": 3100.5},
        )
        assert response.status_code == 201
        assert response.get_json()["employee"]["id"] is not None

        with get_db() as connection:
            row = connection.execute(
                "SELECT * FROM employees WHERE name = %s", ("Zoe",)
            ).fetchone()
        assert row is not None
        assert row["position"] == "Tester"

        assert b"Tester" in client.get("/about").data
        assert len(client.get("/api/employees").get_json()) == 6

    def test_api_add_employee_invalid(self, client):
        with client.session_transaction() as sess:
            sess["logged_in"] = True
        response = client.post(
            "/api/employees",
            json={"name": "", "age": 27, "position": "Tester", "salary": 100},
        )
        assert response.status_code == 400
        assert len(client.get("/api/employees").get_json()) == 5


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
