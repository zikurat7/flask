from flask import Blueprint, jsonify, request

api_bp = Blueprint("api", __name__)


@api_bp.route("/employees", methods=["GET"])
def api_employees():
    employees = [
        {"name": "Alex", "age": 30, "position": "Developer", "salary": 3300},
        {"name": "Mike", "age": 25, "position": "Designer", "salary": 2800},
        {"name": "John", "age": 40, "position": "Manager", "salary": 3600},
        {"name": "Sarah", "age": 28, "position": "Consultant", "salary": 2900},
        {"name": "Emma", "age": 32, "position": "Architect", "salary": 3400},
    ]

    return jsonify(employees)


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

    employee = {
        "name": name.strip(),
        "age": age,
        "position": position.strip(),
        "salary": salary,
    }

    return (
        jsonify({"message": "Employee received successfully", "employee": employee}),
        201,
    )
