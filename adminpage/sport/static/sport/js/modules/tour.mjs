$(function () {

    // localStorage.clear();

    const tour = new Tour({
        framework: "bootstrap4",
        name: 'tour',
        showProgressBar: false,
        showProgressText: false,
        debug: true
    });

    tour.addSteps([
        {
            element: ".tour-step-1",
            placement: "bottom",
            title: "Hello!",
            content: "Welcome to the helpdesk.innopolis.university!<br />" +
                "Here is a small tour to help you navigate the site.",
            path: "/profile/",
            onPrev: function (tour) {
                return false; // There is a bug which allows to click the prev button when on the first step
            }
        },
        {
            element: ".tour-step-2",
            placement: "bottom",
            title: "Sport Groups",
            content: "Here you can choose or change your sport group.",
            path: "/profile/"
        },
        {
            element: ".tour-step-3",
            placement: "bottom",
            title: "Sport Groups",
            content: "You can select from three categories - student clubs, university trainers, and sport complex trainers.<br />" +
                "Hover over the icon to select the group.",
            path: "/category/"
        },
        {
            element: ".tour-step-4-landscape",
            placement: "right",
            title: "Student Club",
            content: "Here you can choose your favorite student club where you want to get hours.",
            path: "/category/"
        },
        {
            element: ".tour-step-4-portrait",
            title: "Student Club",
            content: "Here you can choose your favorite student club where you want to get hours.",
            path: "/category/"
        },
        {
            element: ".tour-step-5-landscape",
            placement: "right",
            title: "IU Trainer",
            content: "Point here if you want to get hours for trainings that university offers you.",
            path: "/category/"
        },
        {
            element: ".tour-step-5-portrait",
            placement: "top",
            title: "IU Trainer",
            content: "Point here if you want to get hours for trainings that university offers you.",
            path: "/category/"
        },
        {
            element: ".tour-step-6-landscape",
            placement: "left",
            title: "SC Trainer",
            content: "Select this if you exercise with sport complex trainers and want to get hours.",
            path: "/category/"
        },
        {
            element: ".tour-step-6-portrait",
            placement: "top",
            title: "SC Trainer",
            content: "Select this if you exercise with sport complex trainers and want to get hours.",
            path: "/category/"
        },
        {
            element: ".tour-step-7",
            placement: "bottom",
            title: "Illness",
            content: "If you are ill, press this to inform your trainers.<br />" +
                "Do not forget to change it back when you are recovered.<br />" +
                "Additionally, you can submit reference to get hours.",
            path: "/profile/",
            onPrev: function (tour) {
                // Based on the width go to the landscape of portrait
                const width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
                if (width > 800) {
                    // Jump to landscape
                    tour.goTo(7);
                    return false;
                }
            },
            onNext: function (tour) {
                return false; // There is a bug which allows to click the next button when on the last step
            }
        }
    ]);

    tour.start();
    // Comment line above and uncomment this to allow touring on every page reload
    // if (tour.ended()) {
    //     tour.restart();
    // } else {
    //     tour.start();
    // }
});