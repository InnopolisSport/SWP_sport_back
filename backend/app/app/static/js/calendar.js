// let f = require("@fullcalendar/core");
// let d = require("@fullcalendar/daygrid");
// let t = require("@fullcalendar/timegrid");

const colors = [
    '#1f77b4',
    '#ff7f0e',
    '#2ca02c',
    '#d62728',
    '#9467bd',
    '#8c564b',
    '#b4005a',
    '#7f7f7f',
    '#7b7c1f',
    '#157786',
];

const color_limit = colors.length;
var color_ptr = 0;

var group_colors = {};

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}


function get_color(group) {
    if (group_colors.hasOwnProperty(group)) {
        // Keep it to assign consistent colors
    } else if (color_ptr < color_limit) {
        // Start assigning colors from the list
        group_colors[group] = colors[color_ptr];
        color_ptr += 1;
        return group_colors[group];
    } else {
        // If it happen that we finished the list - assign random colors
        group_colors[group] = getRandomColor();
    }
    return group_colors[group];

}

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
        .click(() => enroll(event, is_enrolled ? "unenroll" : "enroll"))
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

async function enroll(event, action) {
    const result = await sendResults(`/api/${action}`, {group_id: event.extendedProps.group_id})
    if (result.ok) {
        goto_profile();
    } else {
        update_rendered_events_load(event.extendedProps.group_id, event.extendedProps.capacity);
        toastr.error(result.error.description);
    }
}

function update_rendered_events_load(group_id, load) {
    calendar.getEvents().filter(event => event.extendedProps.group_id === group_id).forEach(
        event => event.setExtendedProp('current_load', load)
    );
}


function render(info) {
    let element = info.el;
    let event = info.event;

    let props = event.extendedProps;
    element.style.fontSize = "99";
    element.style.backgroundColor = (props.current_load >= props.capacity) ? '#f00' : get_color(props.group_id)
    element.style.cursor = 'pointer';

    if (props.training_class) {
        $(element).children(".fc-content").append($(`<div>${props.training_class}</div>`))
    }
}

let calendar
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
        minTime: '08:00:00',
        maxTime: '21:00:00',
        defaultTimedEventDuration: '01:30',
        eventClick: open_modal,
        eventRender: render,
        // Event format: yyyy-mm-dd
        // TODO: at backend use a loop of 10 standard colors as matplotlib do ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        events: '/api/calendar/' + calendarEl.getAttribute('data-sport') + '/schedule'

    });

    calendar.render();
});
