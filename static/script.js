document.addEventListener("DOMContentLoaded", function () {

    // =====================================
    // Flash message auto hide
    // =====================================

    const flashMessages =
        document.querySelectorAll(".flash-message");

    flashMessages.forEach(function (message) {

        setTimeout(function () {

            message.style.opacity = "0";

            message.style.transform =
                "translateX(100%)";

            setTimeout(function () {
                message.remove();
            }, 500);

        }, 3500);

    });


    // =====================================
    // Job search validation
    // =====================================

    const searchForms =
        document.querySelectorAll(
            ".search-box, .filter-box"
        );

    searchForms.forEach(function (form) {

        form.addEventListener(
            "submit",
            function (event) {

                const inputs =
                    form.querySelectorAll("input");

                let hasValue = false;

                inputs.forEach(function (input) {

                    if (
                        input.value.trim() !== ""
                    ) {
                        hasValue = true;
                    }

                });

                if (!hasValue) {

                    event.preventDefault();

                    alert(
                        "Please enter a job title, company, skill or location."
                    );

                }

            }
        );

    });


    // =====================================
    // Apply confirmation
    // =====================================

    const applyForms =
        document.querySelectorAll(
            'form[action^="/apply/"]'
        );

    applyForms.forEach(function (form) {

        form.addEventListener(
            "submit",
            function (event) {

                const confirmed = confirm(
                    "Are you sure you want to apply for this job?"
                );

                if (!confirmed) {
                    event.preventDefault();
                }

            }
        );

    });


    // =====================================
    // Registration validation
    // =====================================

    const registerForm =
        document.getElementById(
            "registerForm"
        );

    if (registerForm) {

        registerForm.addEventListener(
            "submit",
            function (event) {

                const password =
                    document.getElementById(
                        "password"
                    );

                if (
                    password &&
                    password.value.length < 6
                ) {

                    event.preventDefault();

                    alert(
                        "Password must contain at least 6 characters."
                    );

                    password.focus();

                }

            }
        );

    }


    // =====================================
    // Job posting validation
    // =====================================

    const jobForm =
        document.getElementById("jobForm");

    if (jobForm) {

        jobForm.addEventListener(
            "submit",
            function (event) {

                const title =
                    jobForm.querySelector(
                        'input[name="title"]'
                    );

                const description =
                    jobForm.querySelector(
                        'textarea[name="description"]'
                    );

                if (
                    title.value.trim().length < 3
                ) {

                    event.preventDefault();

                    alert(
                        "Job title must contain at least 3 characters."
                    );

                    title.focus();

                    return;
                }

                if (
                    description.value.trim().length < 10
                ) {

                    event.preventDefault();

                    alert(
                        "Please provide a proper job description."
                    );

                    description.focus();

                }

            }
        );

    }


    // =====================================
    // Smooth scrolling
    // =====================================

    document.querySelectorAll(
        'a[href^="#"]'
    ).forEach(function (link) {

        link.addEventListener(
            "click",
            function (event) {

                const target =
                    document.querySelector(
                        link.getAttribute("href")
                    );

                if (target) {

                    event.preventDefault();

                    target.scrollIntoView({
                        behavior: "smooth"
                    });

                }

            }
        );

    });

});
