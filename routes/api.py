from flask import Blueprint, jsonify, request

from db import get_db

api_bp = Blueprint("api", __name__)


def _employee_dict(row):
    """Convert a database row to a JSON-friendly dict (NUMERIC -> int/float)."""
    salary = row["salary"]
    return {
        "id": row["id"],
        "name": row["name"],
        "age": row["age"],
        "position": row["position"],
        "salary": int(salary) if salary == salary.to_integral_value() else float(salary),
    }


def fetch_employees():
    with get_db() as connection:
        rows = connection.execute("SELECT * FROM employees ORDER BY id").fetchall()

    return [_employee_dict(row) for row in rows]


@api_bp.route("/employees", methods=["GET"])
def api_employees():
    return jsonify(fetch_employees())


@api_bp.route("/employees", methods=["POST"])
def add_employee():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON object"}), 400

    name = data.get("name")
    age = data.get("age")
    position = data.get("position")
    salary = data.get("salary")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Valid name is required"}), 400

    if not isinstance(position, str) or not position.strip():
        return jsonify({"error": "Valid position is required"}), 400

    if type(age) is not int or age <= 0:
        return jsonify({"error": "Age must be a positive integer"}), 400

    if type(salary) not in (int, float) or salary < 0:
        return jsonify({"error": "Salary must be a non-negative number"}), 400

    with get_db() as connection:
        row = connection.execute(
            """
            INSERT INTO employees (name, age, position, salary)
            VALUES (%s, %s, %s, %s)
            RETURNING *
            """,
            (name.strip(), age, position.strip(), salary),
        ).fetchone()

    return (
        jsonify(
            {
                "message": "Employee added successfully",
                "employee": _employee_dict(row),
            }
        ),
        201,
    )
