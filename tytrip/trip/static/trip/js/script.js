const myCarouselElement = document.querySelector('#carouselExampleIndicators')

const carousel = new bootstrap.Carousel(myCarouselElement, {
    interval: 5000,
    touch: false
})

document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript загружен"); // Проверка

    const toggleButton = document.getElementById("theme-toggle");
    const body = document.body;

    if (!toggleButton) {
        console.error("Кнопка не найдена!");
        return;
    }

    // Функция установки темы
    function applyTheme(theme) {
        if (theme === "dark") {
            body.classList.add("dark-mode");
            toggleButton.textContent = "☀️ Светлая тема";
        } else {
            body.classList.remove("dark-mode");
            toggleButton.textContent = "🌙 Темная тема";
        }
    }

    // Проверяем сохраненную тему
    const savedTheme = localStorage.getItem("theme") || "light";
    console.log("Сохраненная тема:", savedTheme);
    applyTheme(savedTheme);

    // Обработчик клика
    toggleButton.addEventListener("click", () => {
        const newTheme = body.classList.contains("dark-mode") ? "light" : "dark";
        localStorage.setItem("theme", newTheme);
        applyTheme(newTheme);
    });
});