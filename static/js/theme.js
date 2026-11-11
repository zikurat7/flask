
export function initTheme() {

    const themeButton = document.getElementById("theme-toggle");

    const isDark = document.documentElement.classList.contains("dark-mode");

    if (isDark) {
        document.body.classList.add("dark-mode");
    }

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

    updateThemeButton();
}
