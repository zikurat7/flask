
const themeButton = document.getElementById("theme-toggle");

// Check whether dark mode was saved
const isDark = document.documentElement.classList.contains("dark-mode");

// Apply theme to body as well
if (isDark) {
    document.body.classList.add("dark-mode");
}

// Update button text
function updateThemeButton() {
    const isDark = document.documentElement.classList.contains("dark-mode");

    themeButton.textContent = isDark
        ? "☀️ Light Mode"
        : "🌙 Dark Mode";
}

updateThemeButton();

// Theme switcher
themeButton.addEventListener("click", function () {

    document.documentElement.classList.toggle("dark-mode");
    document.body.classList.toggle("dark-mode");

    const isDark = document.documentElement.classList.contains("dark-mode");

    localStorage.setItem("theme", isDark ? "dark" : "light");

    updateThemeButton();
});

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
