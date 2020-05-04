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

async function enroll(group_id, action) {
    const result = await sendResults(`/api/${action}`, {group_id: group_id})
    if (result.ok) {
        goto_profile();
    } else {
        goto_profile();
        alert(result.error.description);
    }
}


function check_empty(list) {
    if (list.childElementCount === 0) {
        const empty_text_node = document.createElement("a");
        empty_text_node.text = "No clubs are available";
        // empty_text_node.href = "#";
        list.appendChild(empty_text_node);
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
    $('#enroll-unenroll-btn')
        .text(is_enrolled ? "Unenroll" : "Enroll")
        .addClass(is_enrolled ? "btn-danger" : "btn-success")
        .removeClass(is_enrolled ? "btn-success" : "btn-danger")
        .click(() => enroll(group_id, is_enrolled ? "unenroll" : "enroll"))
        .attr('disabled', is_enrolled ? is_primary : current_load === capacity);
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
