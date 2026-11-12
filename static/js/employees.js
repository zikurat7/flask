
export async function initEmployees() {

    let employees = [];

    const employeeContainer = document.getElementById("js-employees");
    const searchInput = document.getElementById("employee-search-input");
    const searchButton = document.getElementById("employee-search-button");
    const searchResult = document.getElementById("employee-search-result");

    const highSalaryButton = document.getElementById("high-salary-button");
    const resetEmployeesButton = document.getElementById("reset-employees-button");
    const sortSalaryButton = document.getElementById("sort-salary-button");
    const averageSalaryButton = document.getElementById("average-salary-button");
    const averageSalaryResult = document.getElementById("average-salary-result");

    // Employee data comes from the database, so escape it before using innerHTML
    function escapeHtml(value) {
        const div = document.createElement("div");
        div.textContent = value;
        return div.innerHTML;
    }

    function displayEmployees(employeeList) {

        if (!employeeContainer) return;

        employeeContainer.innerHTML = "";

        employeeList.forEach(function (employee) {

            employeeContainer.innerHTML += `
                <div class="employee-card">
                    <h2>${escapeHtml(employee.name)}</h2>
                    <p>Age: ${employee.age}</p>
                    <p>Position: ${escapeHtml(employee.position)}</p>
                    <p>Salary: $${employee.salary} per hour</p>
                </div>
            `;

        });
    }

    try {

        const response = await fetch("/api/employees");

        if (!response.ok) {
            throw new Error("Failed to load employees");
        }

        employees = await response.json();

        displayEmployees(employees);

        // Search employees
        function searchEmployees() {

            const searchName = searchInput.value.trim().toLowerCase();

            const foundEmployee = employees.find(employee =>
                employee.name.toLowerCase() === searchName
            );

            if (foundEmployee) {
                searchResult.textContent =
                    `${foundEmployee.name} - ${foundEmployee.position} - $${foundEmployee.salary}`;
            } else {
                searchResult.textContent = "Employee not found.";
            }
        }

        if (searchInput && searchButton && searchResult) {

            searchButton.addEventListener("click", searchEmployees);

            searchInput.addEventListener("keydown", function (event) {
                if (event.key === "Enter") searchEmployees();
            });
        }

        // Filter high salary employees
        if (highSalaryButton) {
            highSalaryButton.addEventListener("click", function () {

                const highSalaryEmployees = employees.filter(employee =>
                    employee.salary > 3000
                );

                displayEmployees(highSalaryEmployees);
            });
        }

        // Reset employee directory
        if (resetEmployeesButton) {
            resetEmployeesButton.addEventListener("click", function () {
                displayEmployees(employees);
            });
        }

        // Sort by highest salary
        if (sortSalaryButton) {
            sortSalaryButton.addEventListener("click", function () {

                const sortedEmployees = [...employees].sort(
                    (a, b) => b.salary - a.salary
                );

                displayEmployees(sortedEmployees);
            });
        }

        // Calculate average salary
        if (averageSalaryButton && averageSalaryResult) {
            averageSalaryButton.addEventListener("click", function () {

                const totalSalary = employees.reduce(
                    (total, employee) => total + employee.salary,
                    0
                );

                const averageSalary = totalSalary / employees.length;

                averageSalaryResult.textContent =
                    `Average salary: $${averageSalary.toFixed(2)} per hour`;
            });
        }

    } catch (error) {
        console.error("Employee loading error:", error);
    }

}


// Add new employee form (admin page)
export function initAddEmployee() {

    const addEmployeeForm = document.getElementById("add-employee-form");
    const addEmployeeResult = document.getElementById("add-employee-result");

    if (!addEmployeeForm || !addEmployeeResult) return;

    addEmployeeForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const name = document.getElementById("new-employee-name").value.trim();
        const age = Number(document.getElementById("new-employee-age").value);
        const position = document.getElementById("new-employee-position").value.trim();
        const salary = Number(document.getElementById("new-employee-salary").value);

        const newEmployee = {
            name: name,
            age: age,
            position: position,
            salary: salary
        };

        try {
            const response = await fetch("/api/employees", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(newEmployee)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || "Failed to add employee");
            }

            addEmployeeResult.textContent = result.message;

            // Clear the form
            addEmployeeForm.reset();

        } catch (error) {
            addEmployeeResult.textContent = error.message;
        }
    });
}
