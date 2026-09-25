document.addEventListener("DOMContentLoaded", () => {

    /* =========================
       HELPERS
    ========================= */

    const showMessage = (element, message, type = "success") => {
        element.textContent = message;
        element.className = `form-message text-${type}`;
    };


    /* =========================
       PASSWORD TOGGLE
    ========================= */

    const password = document.getElementById("password");
    const togglePassword = document.getElementById("togglePassword");

    togglePassword.addEventListener("click", () => {

        const isPassword = password.type === "password";

        password.type = isPassword ? "text" : "password";

        togglePassword.innerHTML = isPassword
            ? '<i class="bi bi-eye-slash"></i>'
            : '<i class="bi bi-eye"></i>';

        togglePassword.setAttribute(
            "aria-label",
            isPassword
                ? "Ocultar contraseña"
                : "Mostrar contraseña"
        );
    });


    /* =========================
       LOGIN
       (validación de formato en el cliente; la autenticación real
       la hace Django al recibir el POST — por eso NO hacemos
       preventDefault cuando el formulario es válido)
    ========================= */

    const loginForm = document.getElementById("loginForm");

    loginForm.addEventListener("submit", (event) => {

        if (!loginForm.checkValidity()) {
            event.preventDefault();
            loginForm.classList.add("was-validated");
            return;
        }

        // Formulario válido: se envía normal (POST a Django).
        // No hacemos event.preventDefault() acá a propósito.
    });


    /* =========================
       GOOGLE LOGIN
    ========================= */

    const googleLogin = document.getElementById("googleLogin");

    googleLogin.addEventListener("click", () => {

        /*
         * DEMO:
         * Para Google real necesitás configurar OAuth
         * (Firebase, Google Identity Services, Auth0, backend propio, etc.).
         */

        googleLogin.disabled = true;

        googleLogin.innerHTML = `
            <span class="spinner-border spinner-border-sm"></span>
            <span>Conectando con Google...</span>
        `;

        setTimeout(() => {

            googleLogin.disabled = false;

            googleLogin.innerHTML = `
                <span class="google-icon">G</span>
                <span>Continuar con Google</span>
            `;

            alert(
                "Demo: acá se conectaría la autenticación real de Google."
            );

        }, 900);
    });


    /* =========================
       REGISTER MODAL
    ========================= */

    const registerModalElement =
        document.getElementById("registerModal");

    const registerModal =
        new bootstrap.Modal(registerModalElement);

    document.getElementById("openRegister")
        .addEventListener("click", () => {
            registerModal.show();
        });


    const registerForm =
        document.getElementById("registerForm");

    const registerMessage =
        document.getElementById("registerMessage");

    registerForm.addEventListener("submit", (event) => {

        event.preventDefault();

        if (!registerForm.checkValidity()) {
            registerForm.classList.add("was-validated");
            return;
        }

        const password1 =
            document.getElementById("registerPassword").value;

        const password2 =
            document.getElementById("registerPassword2").value;

        if (password1 !== password2) {
            showMessage(
                registerMessage,
                "Las contraseñas no coinciden.",
                "danger"
            );
            return;
        }

        showMessage(
            registerMessage,
            "Cuenta lista para registrarse. Conectá este formulario con tu backend.",
            "success"
        );
    });


    /* =========================
       FORGOT PASSWORD
    ========================= */

    const forgotModalElement =
        document.getElementById("forgotModal");

    const forgotModal =
        new bootstrap.Modal(forgotModalElement);

    document.getElementById("forgotPassword")
        .addEventListener("click", (event) => {

            event.preventDefault();

            forgotModal.show();
        });


    const forgotForm =
        document.getElementById("forgotForm");

    const forgotMessage =
        document.getElementById("forgotMessage");

    forgotForm.addEventListener("submit", (event) => {

        event.preventDefault();

        if (!forgotForm.checkValidity()) {
            forgotForm.classList.add("was-validated");
            return;
        }

        showMessage(
            forgotMessage,
            "Si el email existe, recibirás las instrucciones para recuperar tu cuenta.",
            "success"
        );
    });

});