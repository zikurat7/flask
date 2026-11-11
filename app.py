from unicodedata import name

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
user = "Valerii"
age = 28
prof = "Engineer"

app = Flask(__name__)


def init_db():
    connection = sqlite3.connect("messages.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("home.html", user=user, age=age, prof=prof)


@app.route("/about")
def about():
    about_list = [
        {
            "name": "Alex",
            "age": 30,
            "position": "Developer",
            "salary": 3300,
        },
        {
            "name": "Mike",
            "age": 25,
            "position": "Designer",
            "salary": 2800,
        },
        {
            "name": "John",
            "age": 40,
            "position": "Manager",
            "salary": 3600,
        },
    ]
    return render_template("about.html", user=user, prof=prof, about=about_list)


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            return "Please fill in all fields.", 400

        connection = sqlite3.connect("messages.db")

        try:
            connection.execute(
                """
                INSERT INTO messages (name, email, message)
                VALUES (?, ?, ?)
                """,
                (name, email, message),
            )

            connection.commit()

        finally:
            connection.close()

        return render_template("contact_success.html", name=name)

    return render_template("contact.html")


@app.route("/admin/messages")
def admin_messages():

    connection = sqlite3.connect("messages.db")

    connection.row_factory = sqlite3.Row

    messages = connection.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()

    connection.close()

    return render_template("admin_messages.html", messages=messages)


@app.route("/admin/messages/<int:message_id>/delete", methods=["POST"])
def delete_message(message_id):

    connection = sqlite3.connect("messages.db")

    connection.execute("DELETE FROM messages WHERE id = ?", (message_id,))

    connection.commit()
    connection.close()

    return redirect(url_for("admin_messages"))


@app.route("/admin/messages/<int:message_id>/edit", methods=["GET", "POST"])
def edit_message(message_id):

    connection = sqlite3.connect("messages.db")
    connection.row_factory = sqlite3.Row

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            connection.close()
            return "All fields are required.", 400

        connection.execute(
            """
            UPDATE messages
            SET name = ?, email = ?, message = ?
            WHERE id = ?
            """,
            (name, email, message, message_id),
        )

        connection.commit()
        connection.close()

        return redirect(url_for("admin_messages"))

    message = connection.execute(
        "SELECT * FROM messages WHERE id = ?", (message_id,)
    ).fetchone()

    connection.close()

    if message is None:
        return "Message not found", 404

    return render_template("edit_message.html", message=message)


@app.route("/index")
def index():
    return render_template("index.html", user=user, prof=prof)


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
    ]

    return render_template(
        "services.html", services=services_list, age=age, user=user, prof=prof
    )


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5431, debug=False)
