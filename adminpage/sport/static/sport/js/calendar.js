async function open_modal(eventClickInfo) {
    const {event} = eventClickInfo
    const modal = $('#training-info-modal .modal-body');
    modal.empty();
    modal.append($('<div class="spinner-border" role="status"></div>'));
    $('#training-info-modal').modal('show');
    const response = await fetch(`/api/training/${event.extendedProps.id}`, {
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
        .off('click')
        .click(() => enroll(
            event.extendedProps.group_id,
            is_enrolled ? "unenroll" : "enroll",
            set_max_load
        ))
        .attr('disabled', is_enrolled ? is_primary : current_load >= capacity);
    $('#training-info-modal-title').text(`${group_name} training`);
    modal.empty();
    update_rendered_events_load(group_id, current_load);
    if (group_description) {
        modal.append(`<p>${group_description}</p>`)
    }

    const p = modal.append('<p>').children('p:last-child')
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    p.append(`<div>Weekday and time: <strong>${days[event.start.getDay()]}, ${event.start.toJSON().slice(11, 16)}-${event.end.toJSON().slice(11, 16)}</strong></div>`)
    p.append(`<div>Available places: <strong>${capacity - current_load}/${capacity}</strong></div>`)
    if (training_class) {
        p.append(`<div>Class: <strong>${training_class}</strong></div>`)
    }

    if (trainer_first_name || trainer_last_name || trainer_email) {
        modal.append(`<p>Trainer: <strong>${trainer_first_name} ${trainer_last_name}</strong> <a href="mailto:${trainer_email}">${trainer_email}</a></p>`)
    }
}

function set_max_load(group_id) {
    update_rendered_events_load(group_id, 0, true);
}

function update_rendered_events_load(group_id, load, set_max = false) {
    calendar.getEvents().filter(event => event.extendedProps.group_id === group_id).forEach(
        event => event.setExtendedProp(
            'current_load',
            (set_max) ? event.extendedProps.capacity : load
        )
    );
}


function render(info) {
    let element = info.el;
    let event = info.event;

    let props = event.extendedProps;
    element.style.fontSize = "99";
    element.style.backgroundColor = (props.current_load >= props.capacity) ? '#f00' : get_color(props.group_id)
    element.style.cursor = 'pointer';
}

let calendar;
document.addEventListener('DOMContentLoaded', function () {
    let calendarEl = document.getElementById('calendar');

    calendar = new FullCalendar.Calendar(calendarEl, {
        plugins: ['timeGrid'],
        defaultView: 'timeGridWeek',
        header: {
            left: 'title',
            center: '',
            right: ''
            // right: 'today, prev, next'
        },
        height: 'auto',
        timeZone: 'Europe/Moscow',
        firstDay: 1,
        allDaySlot: false,
        slotDuration: '00:30:00',
        minTime: '07:00:00',
        maxTime: '23:00:00',
        defaultTimedEventDuration: '01:30',
        eventClick: open_modal,
        eventRender: render,
        // Event format: yyyy-mm-dd
        events: '/api/calendar/' + calendarEl.getAttribute('data-sport') + '/schedule'

    });

    calendar.render();
});
