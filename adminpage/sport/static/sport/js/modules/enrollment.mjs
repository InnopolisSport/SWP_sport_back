async function  enroll(group_id, action, errorHandler=function(group_id){}) {
    sendResults(`/api/enrollment/${action}`, {group_id: group_id})
        .then(data => {
            goto_profile()
            /* If tour is in process and student unenrolls, having max number of groups,
            * the page reloads together with the tour, thus updating the steps, so the step update is required */
            if (!tour.ended() && $('.tour-step-choice-btn').text().includes('No group choices left')) {
                // Calendar step
                if (tour.getCurrentStepIndex() === 7) {
                    tour.setCurrentStep(15);
                }
            }
        })
        .catch(function (error) {
            errorHandler(group_id);
            toastr.error(error.message);
        })
}