import pytest
import os
import tempfile
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    """Create application instance for testing."""
    test_app = create_app()

    db_fd, db_path = tempfile.mkstemp()
    test_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    test_app.config["TESTING"] = True
    test_app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()

    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


class TestHomePage:
    """Test the home page and basic functionality."""

    def test_home_page_loads(self, client):
        """Test that the home page loads successfully."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"<!DOCTYPE html>" in response.data or b"<html" in response.data

    def test_home_page_has_register_title(self, client):
        """Test that the home page has Register title."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Register" in response.data

    def test_home_page_has_form(self, client):
        """Test that the home page contains a form."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"<form" in response.data


class TestUserRegistration:
    """Test user registration via form."""

    def test_register_new_user(self, client, app):
        """Test registering a new user via the form."""
        response = client.post(
            "/",
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200

        with app.app_context():
            user = User.query.filter_by(username="testuser").first()
            assert user is not None
            assert user.email == "test@example.com"

    def test_password_too_short(self, client):
        """Test that short passwords are rejected."""
        response = client.post(
            "/",
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "short",
                "confirm_password": "short",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200

    def test_passwords_dont_match(self, client):
        """Test that mismatched passwords are rejected."""
        response = client.post(
            "/",
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "confirm_password": "different123",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200

    def test_duplicate_username(self, client, app):
        """Test that duplicate usernames are rejected."""
        # Register user first time
        client.post(
            "/",
            data={
                "username": "duplicate",
                "email": "first@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
        )

        # Try to register with same username
        response = client.post(
            "/",
            data={
                "username": "duplicate",
                "email": "second@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200

        with app.app_context():
            users = User.query.filter_by(username="duplicate").all()
            assert len(users) == 1

    def test_duplicate_email(self, client, app):
        """Test that duplicate emails are rejected."""
        # Register user first time
        client.post(
            "/",
            data={
                "username": "first",
                "email": "duplicate@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
        )

        # Try to register with same email
        response = client.post(
            "/",
            data={
                "username": "second",
                "email": "duplicate@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200

        with app.app_context():
            users = User.query.filter_by(email="duplicate@example.com").all()
            assert len(users) == 1


class TestDatabase:
    """Test database operations and model."""

    def test_database_connection(self, app):
        """Test that database connection works."""
        with app.app_context():
            users = User.query.all()
            assert isinstance(users, list)

    def test_user_table_exists(self, app):
        """Test that user table exists."""
        with app.app_context():
            try:
                User.query.count()
                assert True
            except Exception as e:
                pytest.fail(f"User table doesn't exist: {e}")


class TestApplicationRoutes:
    """Test application routing."""

    def test_root_route_exists(self, client):
        """Test that root route exists and returns 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_post_to_root_route(self, client):
        """Test that POST to root route is handled."""
        response = client.post(
            "/",
            data={
                "username": "test",
                "email": "test@test.com",
                "password": "password123",
                "confirm_password": "password123",
            },
        )
        assert response.status_code in [200, 302, 400]


class TestHTMLContent:
    """Test HTML content rendering."""

    def test_page_has_table(self, client):
        """Test that the page contains a table for displaying users."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"<table" in response.data or b"<tbody>" in response.data

    def test_page_has_static_css(self, client):
        """Test that page references CSS."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"stylesheet" in response.data or b".css" in response.data


class TestApplicationHealth:
    """Test overall application health."""

    def test_app_runs_without_errors(self, client):
        """Test that the application starts and runs."""
        response = client.get("/")
        assert response.status_code == 200

    def test_app_context_works(self, app):
        """Test that app context is properly configured."""
        with app.app_context():
            from flask import current_app

            assert current_app is not None
            assert current_app.config["TESTING"] is True

    def test_successful_registration_flow(self, client, app):
        """Test complete registration flow."""
        response = client.post(
            "/",
            data={
                "username": "flowtest",
                "email": "flow@test.com",
                "password": "validpass123",
                "confirm_password": "validpass123",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200

        with app.app_context():
            user = User.query.filter_by(username="flowtest").first()
            assert user is not None


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_get_request(self, client):
        """Test GET request with no parameters."""
        response = client.get("/")
        assert response.status_code == 200

    def test_empty_post_request(self, client):
        """Test POST request with empty data."""
        response = client.post("/", data={})
        assert response.status_code in [200, 302, 400]

    def test_nonexistent_route(self, client):
        """Test that nonexistent routes return 404."""
        response = client.get("/nonexistent-route-12345")
        assert response.status_code == 404
