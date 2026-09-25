// =========================
// LOGIN
// =========================

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", function (event) {

        event.preventDefault();

        alert(
            "Inicio de sesión de ejemplo.\n\n" +
            "Más adelante este formulario se conectará con Django."
        );

    });

}


// =========================
// REGISTRO
// =========================

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", function (event) {

        event.preventDefault();

        alert(
            "Registro de ejemplo.\n\n" +
            "Más adelante este formulario se conectará con el backend Django."
        );

    });

}


// =========================
// NAVBAR
// Cerrar menú mobile al
// seleccionar una sección
// =========================

const navLinks = document.querySelectorAll(
    ".navbar-nav .nav-link"
);

const navbarCollapse = document.querySelector(
    ".navbar-collapse"
);

navLinks.forEach(function (link) {

    link.addEventListener("click", function () {

        if (
            navbarCollapse.classList.contains("show")
        ) {

            const bsCollapse =
                bootstrap.Collapse.getInstance(
                    navbarCollapse
                );

            if (bsCollapse) {
                bsCollapse.hide();
            }

        }

    });

});


// =========================
// ANIMACIÓN AL HACER SCROLL
// =========================

const animatedElements = document.querySelectorAll(
    ".feature-card, .value-card, .step-card, .benefit-card, .problem-card"
);

const observer = new IntersectionObserver(
    function (entries) {

        entries.forEach(function (entry) {

            if (entry.isIntersecting) {

                entry.target.style.opacity = "1";
                entry.target.style.transform =
                    "translateY(0)";

                observer.unobserve(entry.target);

            }

        });

    },
    {
        threshold: 0.1
    }
);


animatedElements.forEach(function (element) {

    element.style.opacity = "0";

    element.style.transform =
        "translateY(20px)";

    element.style.transition =
        "opacity 0.5s ease, transform 0.5s ease";

    observer.observe(element);

});