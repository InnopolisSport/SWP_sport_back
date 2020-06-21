$(function () {
    const tour = new Tour({
        framework: "bootstrap4",
        name: 'tour',
        showProgressBar: false,
        showProgressText: false,
        backdrop: true,
        debug: true
    });

    tour.addSteps([
        {
            element: ".tour-step-1",
            placement: "bottom",
            orphan: true, // Center the popover
            title: "Hello!",
            content: "Welcome to the helpdesk.innopolis.university!<br />" +
                "Here is a small tour to help you navigate the site.",
            path: "/profile/"
        },
        {
            element: ".tour-step-2",
            placement: "bottom",
            reflex: true, // Continue only on button click
            reflexOnly: true,
            title: "Sport Groups",
            content: "Here you can choose or change your sport group. <strong>Click it!</strong>",
            path: "/profile/",
        },
        {
            element: ".tour-step-3",
            placement: "right",
            title: "Sport Groups",
            content: "You can select from three categories - student clubs, university trainers, and sport complex trainers.",
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
            placement: "right",
            title: "IU Trainer",
            content: "Point here if you want to get hours for trainings that university offers you.",
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
            content: "Point here if you want to get hours for trainings that university offers you.",
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
        },
        {
            element: ".tour-step-7",
            placement: "bottom",
            title: "Illness",
            content: "If you are ill, press this to inform your trainers.<br />" +
                "Do not forget to change status back when you are recovered.<br />" +
                "Additionally, you can submit reference to get hours.",
            path: "/profile/",
            onPrev: function (tour) {
                // Based on the width go to the landscape or portrait
                const width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
                if (width > 800) {
                    // Jump to landscape
                    tour.goTo(7);
                    return false;
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
    ]);

    // If calendar is shown on the page
    if (document.getElementById("calendar")) {
        tour.addSteps([
            {
                element: ".tour-step-8",
                placement: "top",
                title: "Calendar",
                content: "This is your schedule. You can find all your trainings there.<br />" +
                    "You can click on the training to check out details such as trainer contacts or the place of training.",
                path: "/profile/"
            },
            {
                element: ".fc-right",
                placement: "top",
                title: "Calendar",
                content: "You can navigate through the calendar using these buttons.",
                path: "/profile/"
            }
        ]);
    }

    tour.addStep({
        element: ".tour-step-1",
        placement: "bottom",
        orphan: true,
        title: "Thank you!",
        content: "Thank you for your patience! Now you know how to use this site!",
        path: "/profile/"
    });

    tour.start();
    // Comment line above and uncomment this to allow touring on every page reload
    // if (tour.ended()) {
    //     tour.restart();
    // } else {
    //     tour.start();
    // }
});

// function disableObject (tour) {
//     const step = tour.getStep(tour._current);
//     $(step.element).addClass("disabled-object");
// }
//
// function enableObject (tour) {
//     const step = tour.getStep(tour._current);
//     $(step.element)[0].className =
//         $(step.element)[0].className.replace(/\bdisabled-object\b/g, ""); // Cross-browser solution for removing a class
// }