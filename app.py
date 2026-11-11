from flask import Flask, render_template

app = Flask(__name__)
user = "Valerii"
age = 28
prof = "Engineer"


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


@app.route("/contact")
def contact():
    return render_template("contact.html", user=user, prof=prof)


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
    app.run(host="0.0.0.0", port=5431, debug=False)
