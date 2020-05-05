async function sendResults(url, data) {
    let response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        // headers: {
        //     // 'Content-Type': 'application/json'
        // }
    });
    return await response.json();
}

function goto_profile() {
    window.location.href = "/profile";
}

function mark_club_as_full(club_id) {
    $(`#club-${club_id}`).remove().insertAfter($(".club-dropdown a:last-child")).children('a span').text('0');
}

function mark_club_as_free(club_id, free_places) {
    const elem = $(`#club-${club_id}`)
    if (elem.children('a span').text() === '0') {
        elem.remove().insertBefore($(".club-dropdown a:first-child")).children('a span').text(free_places.toString());
    }
}

async function enroll(group_id, action) {
    const result = await sendResults(`/api/${action}`, {group_id: group_id})
    if (result.ok) {
        goto_profile();
    } else {
        if (result.error.code === 2) { // full group
            mark_club_as_full(group_id)
        }
        alert(result.error.description);
    }
}

async function open_modal(id) {
    const modal = $('#training-info-modal .modal-body');
    modal.empty();
    modal.append($('<div class="spinner-border" role="status"></div>'));
    $('#training-info-modal').modal('show');
    const response = await fetch(`/api/group/${id}`, {
        method: 'GET'
    });
    const {
        group_id,
        group_name,
        group_description,
        trainer_first_name,
        trainer_last_name,
        trainer_email,
        is_enrolled,
        capacity,
        current_load,
        training_class,
        is_primary
    } = await response.json();
    if (current_load >= capacity) {
        mark_club_as_full(group_id)
    } else {
        mark_club_as_free(group_id, capacity - current_load)
    }
    $('#enroll-unenroll-btn')
        .text(is_enrolled ? "Unenroll" : "Enroll")
        .addClass(is_enrolled ? "btn-danger" : "btn-success")
        .removeClass(is_enrolled ? "btn-success" : "btn-danger")
        .off('click')
        .click(() => enroll(group_id, is_enrolled ? "unenroll" : "enroll"))
        .prop('disabled', is_enrolled ? is_primary : current_load >= capacity);
    $('#training-info-modal-title').text(`${group_name} group`);
    modal.empty();
    if (group_description) {
        modal.append(`<p>${group_description}</p>`)
    }

    const p = modal.append('<p>').children('p:last-child')
    p.append(`<div>Available places: <strong>${capacity - current_load}/${capacity}</strong></div>`)
    if (training_class) {
        p.append(`<div>Class: <strong>${training_class}</strong></div>`)
    }

    if (trainer_first_name || trainer_last_name || trainer_email) {
        modal.append(`<p>Trainer: <strong>${trainer_first_name} ${trainer_last_name}</strong> <a href="mailto:${trainer_email}">${trainer_email}</a></p>`)
    }
}
