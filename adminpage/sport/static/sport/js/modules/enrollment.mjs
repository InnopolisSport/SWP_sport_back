async function enroll(group_id, action, errorHandler=function(group_id){}) {
    sendResults(`/django/api/enrollment/${action}`, {group_id: group_id})
        .then(data => {
            goto_profile()
        })
        .catch(function (error) {
            errorHandler(group_id);
            toastr.error(error.message);
        })
}