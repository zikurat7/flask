import os
from functools import wraps

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)
from werkzeug.security import check_password_hash

from db import get_db
from routes.api import api_bp, fetch_employees

# Load environment variables
load_dotenv()

# Create Flask application
app = Flask(__name__)

# Configure secret key
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Register API Blueprint
app.register_blueprint(api_bp, url_prefix="/api")

# Admin credentials
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

# Employees inserted on first startup
SEED_EMPLOYEES = [
    ("Alex", 30, "Developer", 3300),
    ("Mike", 25, "Designer", 2800),
    ("John", 40, "Manager", 3600),
    ("Sarah", 28, "Consultant", 2900),
    ("Emma", 32, "Architect", 3400),
]

# Website variables
user = "Valerii"
age = 28
prof = "Engineer"


def init_db():
    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK (age > 0),
                position TEXT NOT NULL,
                salary NUMERIC(10, 2) NOT NULL CHECK (salary >= 0)
            )
        """)

        # Seed the initial team only when the table is empty
        count = connection.execute("SELECT COUNT(*) AS n FROM employees").fetchone()
        if count["n"] == 0:
            with connection.cursor() as cursor:
                cursor.executemany(
                    """
                    INSERT INTO employees (name, age, position, salary)
                    VALUES (%s, %s, %s, %s)
                    """,
                    SEED_EMPLOYEES,
                )


def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if not session.get("logged_in"):
            return redirect(url_for("login"))

        return function(*args, **kwargs)

    return wrapper


@app.route("/admin/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and check_password_hash(
            ADMIN_PASSWORD_HASH, password
        ):

            session["logged_in"] = True
            flash("Successfully logged in!", "success")
            return redirect(url_for("admin_messages"))

        flash("Invalid username or password", "error")
        return render_template("login.html"), 401

    return render_template("login.html")


@app.route("/")
def home():
    return render_template("home.html", user=user, age=age, prof=prof)


@app.route("/about")
def about():
    about_list = fetch_employees()
    return render_template("about.html", user=user, prof=prof, about=about_list)


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            return "Please fill in all fields.", 400

        with get_db() as connection:
            connection.execute(
                """
                INSERT INTO messages (name, email, message)
                VALUES (%s, %s, %s)
                """,
                (name, email, message),
            )

        return render_template("contact_success.html", name=name)

    return render_template("contact.html")


@app.route("/admin/messages")
@login_required
def admin_messages():

    with get_db() as connection:
        messages = connection.execute(
            "SELECT * FROM messages ORDER BY id DESC"
        ).fetchall()

    return render_template("admin_messages.html", messages=messages)


@app.route("/admin/messages/<int:message_id>/delete", methods=["POST"])
@login_required
def delete_message(message_id):

    with get_db() as connection:
        connection.execute("DELETE FROM messages WHERE id = %s", (message_id,))

    flash("Message successfully deleted!", "success")
    return redirect(url_for("admin_messages"))


@app.route("/admin/messages/<int:message_id>/edit", methods=["GET", "POST"])
@login_required
def edit_message(message_id):

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            return "All fields are required.", 400

        with get_db() as connection:
            connection.execute(
                """
                UPDATE messages
                SET name = %s, email = %s, message = %s
                WHERE id = %s
                """,
                (name, email, message, message_id),
            )

        flash("Message successfully updated!", "success")
        return redirect(url_for("admin_messages"))

    with get_db() as connection:
        message = connection.execute(
            "SELECT * FROM messages WHERE id = %s", (message_id,)
        ).fetchone()

    if message is None:
        return "Message not found", 404

    return render_template("edit_message.html", message=message)


@app.route("/index")
def index():
    return render_template("index.html", user=user, prof=prof)


@app.route("/admin/logout", methods=["POST"])
@login_required
def logout():

    session.clear()
    flash("Successfully logged out!", "success")
    return redirect(url_for("login"))


@app.route("/services")
def services():
    services_list = [
        {
            "name": "Construction",
            "description": "Building new structures",
            "price": 300,
        },
        {
            "name": "Renovation",
            "description": "Updating existing structures",
            "price": 200,
        },
        {
            "name": "Maintenance",
            "description": "Regular upkeep and repairs",
            "price": 100,
        },
        {
            "name": "Inspection",
            "description": "Thorough examination of structures",
            "price": 120,
        },
        {
            "name": "Consultation",
            "description": "Expert advice for your projects",
            "price": 150,
        },
        {
            "name": "Design",
            "description": "Architectural and interior design services",
            "price": 250,
        },
        {
            "name": "Project Management",
            "description": "Overseeing and coordinating construction projects",
            "price": 350,
        },
    ]

    return render_template(
        "services.html", services=services_list, age=age, user=user, prof=prof
    )


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000, debug=False)
