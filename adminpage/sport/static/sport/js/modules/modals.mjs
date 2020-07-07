function prepareModal(id, size = 'modal-md') {
    const modal = $(id);
    modal.addClass('modal')
        .addClass('fade')
        .attr('tabindex', '-1')
        .attr('role', 'dialog')
        .attr('aria-labelledby', `${id}-title`);
    modal.html(`<div class="modal-dialog ${size}" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="${id}-title"></h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body text-left"></div>
          <div class="modal-footer"></div>
        </div>
      </div>`)
}


async function openModal(id, apiUrl) {
    const modal = $(id)
    const title = modal.find('.modal-title');
    const body = modal.find('.modal-body');
    const footer = modal.find('.modal-footer');
    body.empty();
    footer.empty();
    body.append($('<div class="spinner-border" role="status"></div>'));
    title.text('Loading...');
    modal.modal('show');
    let data;
    if (apiUrl) {
        const response = await fetch(apiUrl, {
            method: 'GET'
        });
        data = await response.json();
    }else{
        data = null;
    }
    body.empty();
    return {data, title, body, footer};
}

function renderGroupModalBody(body, data) {
    const {
        group_description, trainer_first_name, trainer_last_name, trainer_email, capacity, current_load, training_class
    } = data;
    if (group_description) {
        body.append(`<p>${group_description}</p>`);
    }

    const p = body.append('<p>').children('p:last-child');
    p.append(`<div>Available places: <strong>${capacity - current_load}/${capacity}</strong></div>`);
    if (training_class) {
        p.append(`<div>Class: <strong>${training_class}</strong></div>`);
    }

    if (trainer_first_name || trainer_last_name || trainer_email) {
        body.append(`<p>Trainer: 
                        <strong>${trainer_first_name} ${trainer_last_name}</strong> 
                        <a href="mailto:${trainer_email}">${trainer_email}</a>
                     </p>`);
    }
}

function formatTime(time) {
    return time.substring(0, time.length - 3);
}

async function openGroupInfoModalForStudent(apiUrl, enrollErrorCb = () => 0) {
    const {data, title, body, footer} = await openModal('#group-info-modal', apiUrl)
    const {group_id, group_name, is_enrolled, capacity, current_load, is_primary, schedule} = data;

    let disabled_attr;

    if (is_enrolled) {
        disabled_attr =  is_primary ? 'disabled' : '';
        footer.html(`
            <div class="container">
                <div class="row justify-content-between">
                    <div><button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button></div>
                    <div><button type="button" class="btn btn-danger ${disabled_attr}" ${disabled_attr}>Unenroll</button></div>
                </div>
            </div>
        `);
        footer.find('.btn-danger').click(() => enroll(group_id, 'unenroll'));
    } else {
        disabled_attr = current_load >= capacity ? 'disabled' : ''
        footer.html(`
            <div class="container">
                <div class="row justify-content-between">
                    <div><button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button></div>
                    <div><button type="button" class="btn btn-success ${disabled_attr}" ${disabled_attr}>Enroll</button></div>
                </div>
            </div>
        `);
        footer.find('.btn-success').click(() => enroll(group_id, 'enroll', enrollErrorCb));
    }
    title.text(`${group_name} group`);
    renderGroupModalBody(body, data)
    if (schedule && schedule.length > 0) {

        const days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ];
        schedule.sort(
            (a, b) => (a.weekday > b.weekday) ? 1 : (a.start > b.start) ? 1 : -1
        )
        body.append(`
            <strong>Schedule</strong>:<br>    
        `)

        let currentDay = null;

        for (let training of schedule) {
            if (training.weekday !== currentDay) {
                body.append(`<i>${days[training.weekday]}</i>:`);
                currentDay = training.weekday;
            }
            body.append(`<li>${formatTime(training.start)} - ${formatTime(training.end)}</li>`);
        }

    }
    return data;
}

async function openGroupInfoModalForTrainer(apiUrl) {
    const {data, title, body, footer} = await openModal('#group-info-modal', apiUrl)
    footer.html('<div><button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button></div>');
    title.text(`${data.group_name} group`);
    renderGroupModalBody(body, data)
}
