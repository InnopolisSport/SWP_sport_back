const tour = new Tour({
    framework: "bootstrap4",
    name: 'main-tour',
    showProgressBar: false,
    showProgressText: false,
    backdrop: true,
    debug: true
});

$(function () {
    // First step
    tour.addStep(
        {
            element: ".tour-step-1",
            orphan: true, // Center the popover
            title: "Hello!",
            content: "Welcome to the helpdesk.innopolis.university!<br />" +
                "Here is a small tour to help you navigate the site.",
            path: "/profile/"
        }
    );

    // For trainers
    tour.addStep(
        {
            element: "#trainer-list",
            placement: "bottom",
            title: "Sport Groups",
            content: "It is the list of sports groups you train.",
            path: "/profile/"
        }
    );

    // For students
    tour.addSteps([
        {
            element: "#student-list",
            placement: "bottom",
            title: "Sport Groups",
            content: "It is the list of sports groups you joined.",
            path: "/profile/"
        },
        {
            element: "#semester-hours",
            placement: "bottom",
            title: "Attendance",
            content: "You can see all your graded activities in the current semester here. " +
                "As soon as the trainer marks your attendance, you will see it.",
            path: "/profile"
        }
    ]);

    /* If there is no such element, the tour will skip the step */
    // If student can enroll
    if (!$(".tour-step-2.disabled").length || document.URL.includes("/category/")) {
        tour.addSteps([
            {
                element: ".tour-step-2",
                placement: "bottom",
                reflex: true, // Continue only on button click
                reflexOnly: true,
                title: "Sport Groups",
                content: "Here you can choose your sports group. <strong>Click it!</strong>",
                path: "/profile/",
            },
            {
                element: ".tour-step-3",
                orphan: true,
                title: "Sport Groups",
                content: "You can select from three categories - <strong>student clubs</strong>, " +
                    "<strong>university trainers</strong>, and <strong>sport complex trainers</strong>.",
                path: "/category/"
            },
            {
                element: ".tour-step-4-landscape",
                placement: "right",
                title: "Student Club",
                content: "Here you can choose your favorite student club where you want to get hours.",
                path: "/category/",
                onShown: function (tour) {
                    const step = tour.getStep(tour._current);
                    $(step.element).addClass("disabled-object");
                },
                onHidden: function (tour) {
                    const step = tour.getStep(tour._current);
                    $(step.element)[0].className =
                        $(step.element)[0].className.replace(/\bdisabled-object\b/g, ""); // Cross-browser solution for removing a class
                }
            },
            {
                element: ".tour-step-4-portrait",
                placement: "bottom",
                title: "Student Club",
                content: "Here you can choose your favorite student club where you want to get hours.",
                path: "/category/",
                onShown: function (tour) {
                    const step = tour.getStep(tour._current);
                    $(step.element).addClass("disabled-object");
                },
                onHidden: function (tour) {
                    const step = tour.getStep(tour._current);
                    $(step.element)[0].className =
                        $(step.element)[0].className.replace(/\bdisabled-object\b/g, ""); // Cross-browser solution for removing a class
                }
            },
            {
                element: ".tour-step-5-landscape",
                placement: "left",
                title: "IU Trainer",
                content: "Point here if you want to get hours for sports classes that the university offers you.",
                path: "/category/",
                onShown: function (tour) {
                    const step = tour.getStep(tour._current);
                    $(step.element).addClass("disabled-object");
                },
                onHidden: function (tour) {
                    const step = tour.getStep(tour._current);
                    $(step.element)[0].className =
                        $(step.element)[0].className.replace(/\bdisabled-object\b/g, ""); // Cross-browser solution for removing a class
                }
            },
            {
                element: ".tour-step-5-portrait",
                placement: "top",
                title: "IU Trainer",
                content: "Point here if you want to get hours for sports classes that university offers you.",
                path: "/category/",
                onShown: function (tour) {
                    const step = tour.getStep(tour._current);
                    $(step.element).addClass("disabled-object");
                },
                onHidden: function (tour) {
                    const step = tour.getStep(tour._current);
                    $(step.element)[0].className =
                        $(step.element)[0].className.replace(/\bdisabled-object\b/g, ""); // Cross-browser solution for removing a class
                }
            },
            {
                element: ".tour-step-6-landscape",
                placement: "left",
                title: "SC Trainer",
                content: "Select this if you exercise with sport complex trainers and want to get hours.",
                path: "/category/",
                onShown: function (tour) {
                    const step = tour.getStep(tour._current);
                    $(step.element).addClass("disabled-object");
                },
                onHidden: function (tour) {
                    const step = tour.getStep(tour._current);
                    $(step.element)[0].className =
                        $(step.element)[0].className.replace(/\bdisabled-object\b/g, ""); // Cross-browser solution for removing a class
                }
            },
            {
                element: ".tour-step-6-portrait",
                placement: "top",
                title: "SC Trainer",
                content: "Select this if you exercise with sport complex trainers and want to get hours.",
                path: "/category/",
                onShown: function (tour) {
                    const step = tour.getStep(tour._current);
                    $(step.element).addClass("disabled-object");
                },
                onHidden: function (tour) {
                    const step = tour.getStep(tour._current);
                    $(step.element)[0].className =
                        $(step.element)[0].className.replace(/\bdisabled-object\b/g, ""); // Cross-browser solution for removing a class
                }
            }
        ]);
    } else {
        // If student cannot enroll
        tour.addStep(
            {
                element: ".tour-step-2",
                placement: "bottom",
                title: "Sport Groups",
                content: "Here you can choose your sports group.<br />Unfortunately, you have chosen the maximum number of groups. " +
                    "Unenroll to pick a new group.",
                path: "/profile/"
            }
        );
    }

    // Ill button
    tour.addStep(
        {
            element: ".tour-step-7",
            placement: "bottom",
            title: "Illness",
            content: "If you are ill, press this to inform your trainers.<br />" +
                "Do not forget to change the status back when you recover.<br />" +
                "Additionally, you can submit a reference to get hours.",
            path: "/profile/",
            onPrev: function (tour) {
                /* If student can enroll */
                if (!$(".tour-step-2.disabled").length) {
                    // Based on the width go to the landscape or portrait
                    const width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
                    if (width > 800) {
                        // Jump to landscape
                        tour.goTo(10);
                        return false;
                    } else {
                        // Jump to portrait
                        return true;
                    }
                } else {
                    return true;
                }
            },
            onShown: function (tour) {
                const step = tour.getStep(tour._current);
                $(step.element).addClass("disabled-object");
            },
            onHidden: function (tour) {
                const step = tour.getStep(tour._current);
                $(step.element)[0].className =
                    $(step.element)[0].className.replace(/\bdisabled-object\b/g, ""); // Cross-browser solution for removing a class
            }
        }
    );

    /* If calendar is shown on the page */
    // For both students and trainers
    if (document.getElementById("student-span") && document.getElementById("trainer-span")) {
        tour.addStep(
            {
                element: ".tour-step-8",
                placement: "auto",
                title: "Calendar",
                content: "It is your schedule. You can find all your sports classes there.<br />" +
                    "There are <strong>two types of events - with and without the icon.</strong><br /><br />" +
                    "Events <strong>without the icon</strong> are the ones you joined. " +
                    "You can click on the training to check out details such as trainer contacts or location.<br /><br />" +
                    "Events <strong>with the icon</strong> are the ones you train. You can click on the training to mark attendance.",
                path: "/profile/",
                onShown: function (tour) {
                    const step = tour.getStep(tour._current);
                    $(step.element)[0].scrollIntoView(false);
                }
            }
        );
    } else {
        // For only trainers
        if (document.getElementById("trainer-span")) {
            tour.addStep(
                {
                    element: ".tour-step-8",
                    placement: "auto",
                    title: "Calendar",
                    content: "It is your schedule. You can find all your sports classes there.<br />" +
                        "You can click on the training to mark attendance.",
                    path: "/profile/",
                    onShown: function (tour) {
                        const step = tour.getStep(tour._current);
                        $(step.element)[0].scrollIntoView(false);
                    }
                }
            );
        } else {
            // For only students
            tour.addStep(
                {
                    element: ".tour-step-8",
                    placement: "auto",
                    title: "Calendar",
                    content: "It is your schedule. You can find all your sports classes there.<br />" +
                        "You can click on the training to check out details such as trainer contacts or location.",
                    path: "/profile/",
                    onShown: function (tour) {
                        const step = tour.getStep(tour._current);
                        $(step.element)[0].scrollIntoView(false);
                    }
                }
            );
        }
    }
    // For all
    tour.addStep(
        {
            element: ".fc-right",
            placement: "top",
            title: "Calendar",
            content: "You can navigate through the calendar using these buttons.",
            path: "/profile/"
        }
    );

    // Highlight "?" button
    tour.addStep(
        {
            element: "#help-btn",
            placement: "bottom",
            title: "Help",
            content: "Forgot something? Consider clicking this to repeat the tour.",
            path: "/profile/",
            onShown: function (tour) {
                $("#tourHighlight").css("opacity", 0);
            }
        }
    );

    // Last step
    tour.addStep(
        {
            element: ".tour-step-1",
            orphan: true,
            title: "Thank You!",
            content: "Thank you for your patience! Now you know how to use this site!",
            path: "/profile/"
        }
    );

    tour.start();
});

function start_tour() {
    if (tour.ended()) {
        tour.restart();
    } else {
        tour.start();
    }
}