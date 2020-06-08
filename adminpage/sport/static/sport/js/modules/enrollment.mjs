async function enroll(group_id, action) {
    sendResults(`/django/api/enrollment/${action}`, {group_id: group_id})
        .then(data => {
            goto_profile()
        })
        .catch(function (error) {
            toastr.error(error.message);
        })
}