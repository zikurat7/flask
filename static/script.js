
import { initTheme } from "./js/theme.js";
import { initEmployees, initAddEmployee } from "./js/employees.js";

// Initialize modules
initTheme();
initEmployees();
initAddEmployee();


// ==========================
// CLICK COUNTER
// ==========================

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


// ==========================
// CONTACT FORM VALIDATION
// ==========================

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
