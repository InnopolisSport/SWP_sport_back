async function  enroll(group_id, action, errorHandler=function(group_id){}) {
    sendResults(`/api/enrollment/${action}`, {group_id: group_id})
        .then(data => {
            goto_profile()
            // If tour is in process and student unenrolls, having max number of groups,
            // the page reloads together with the tour, thus updating the steps, so the step update is required
            if (!tour.ended() && $('.tour-step-choice-btn').text().includes('No group choices left')) {
                if (tour.getCurrentStepIndex() === 7) {
                    tour.setCurrentStep(15);
                }
            } else
                // When only two calendar steps are shown, and student has only one group (secondary - student cannot unenroll from primary group)
                // e.g. calendar will be removed from page after reloading
                if (!tour.ended() && $('.tour-step-choice-btn').text().includes('2 group choices left') &&
                    (localStorage.getItem("main-tour_calendar") === "false")) {
                tour.end();
            }
        })
        .catch(function (error) {
            errorHandler(group_id);
            toastr.error(error.message);
        })
}