let employees = [];

const themeButton = document.getElementById("theme-toggle");

// Check whether dark mode was saved
const isDark = document.documentElement.classList.contains("dark-mode");

// Apply theme to body as well
if (isDark) {
    document.body.classList.add("dark-mode");
}

// Update button text
function updateThemeButton() {
    if (!themeButton) return;

    const isDark = document.documentElement.classList.contains("dark-mode");

    themeButton.textContent = isDark
        ? "☀️ Light Mode"
        : "🌙 Dark Mode";
}
if (themeButton) {
    themeButton.addEventListener("click", function () {

        document.documentElement.classList.toggle("dark-mode");
        document.body.classList.toggle("dark-mode");

        const isDark = document.documentElement.classList.contains("dark-mode");

        localStorage.setItem("theme", isDark ? "dark" : "light");

        updateThemeButton();
    });
}
// Click Counter

let count = 0;

const counterButton = document.getElementById("counter-button");
const counterDisplay = document.getElementById("counter");
const resetButton = document.getElementById("reset-button");

if (counterButton && counterDisplay) {

    // Increase counter
    counterButton.addEventListener("click", function () {
        count++;
        counterDisplay.textContent = count;
    });

    // Reset counter
    if (resetButton) {
        resetButton.addEventListener("click", function () {
            count = 0;
            counterDisplay.textContent = count;
        });
    }
}

// Contact Form Validation

const contactForm = document.getElementById("contact-form");

if (contactForm) {

    contactForm.addEventListener("submit", function (event) {

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const message = document.getElementById("message").value.trim();

        const errorDisplay = document.getElementById("form-error");

        if (name === "" || email === "" || message === "") {

            event.preventDefault();

            errorDisplay.textContent = "Please fill in all fields.";
            errorDisplay.style.color = "red";

        } else if (message.length < 10) {

            event.preventDefault();

            errorDisplay.textContent = "Your message must contain at least 10 characters.";
            errorDisplay.style.color = "red";

        } else {

            errorDisplay.textContent = "";

        }

    });

}

const searchInput = document.getElementById("employee-search-input");
const searchButton = document.getElementById("employee-search-button");
const searchResult = document.getElementById("employee-search-result");

// empoyee data

if (searchInput && searchButton && searchResult) {

    searchButton.addEventListener("click", function () {

        const searchName = searchInput.value.trim().toLowerCase();

        const foundEmployee = employees.find(function (employee) {
            return employee.name.toLowerCase() === searchName;
        });

        if (foundEmployee) {

            searchResult.innerHTML = `
                <div class="employee-card">
                    <h2>${foundEmployee.name}</h2>
                    <p>Age: ${foundEmployee.age}</p>
                    <p>Position: ${foundEmployee.position}</p>
                    <p>Salary: $${foundEmployee.salary} per hour</p>
                </div>
            `;

        } else {
            searchResult.textContent = "Employee not found.";
        }
    });
}

async function getEmployees() {

    try {

        const response = await fetch("/api/employees");

        if (!response.ok) {
            throw new Error("Failed to load employees");
        }

        employees = await response.json();

        console.log("Employees received from Flask:", employees);

        displayEmployees(employees);

    } catch (error) {

        console.error("Error:", error);

    }

}
function displayEmployees(employees) {

    const employeeContainer = document.getElementById("js-employees");

    if (!employeeContainer) return;

    employeeContainer.innerHTML = "";

    employees.forEach(function (employee) {

        employeeContainer.innerHTML += `
            <div class="employee-card">
                <h2>${employee.name}</h2>
                <p>Age: ${employee.age}</p>
                <p>Position: ${employee.position}</p>
                <p>Salary: $${employee.salary} per hour</p>
            </div>
        `;

    });

}
getEmployees();