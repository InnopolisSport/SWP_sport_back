async function sendResults(url, data) {
    let response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
    });
    return await response.json();
}

function goto_profile() {
    window.location.href = "/profile";
}

function make_hours_table(trainings) {
    const table = $('<table class="table table-hover">');
    table.append('<thead>')
        .children('thead')
        .append('<tr />')
        .children('tr')
        .append('<th scope="col">Group</th><th scope="col">Date</th><th scope="col">Hours</th>');
    const tbody = table.append('<tbody>').children('tbody');
    trainings.forEach(({group, timestamp, hours}) => {
        tbody.append($(`<tr>
                            <td>${group}</td>
                            <td>${timestamp.substr(0, 16)}</td>
                            <td>${hours}</td>
                        </tr>`))
    });
    return table;
}

const loaded_hours = {};

async function fetch_detailed_hours(e) {
    const semester_id = parseInt(e.getAttribute('data-semester-id'), 10);
    if (loaded_hours[semester_id]) return;
    const response = await fetch(`/api/profile/history/${semester_id}`, {
        method: 'GET'
    });
    const history = await response.json();
    const table = $(`#hours-modal-${semester_id} .modal-body`);
    table.empty();
    table.append(make_hours_table(history.trainings));
    loaded_hours[semester_id] = true;
}

function toggle_ill(elem) {
    sendResults("/api/profile/sick/toggle", {})
        .then(data => {
            if (data.ok) {
                goto_profile();
            } else {
                switch (data.error.code) {
                    case 1:
                        break;
                }
                alert(data.error.description);
            }
        })


}

/*
    Calendar
*/
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

function clearColors(info) {
    group_colors.clear;
    color_ptr = 0;
}

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


function render(info) {
    let element = info.el;
    let event = info.event;

    let props = event.extendedProps;
    element.style.fontSize = "99";
    element.style.backgroundColor = get_color(props.id);
    if (props.can_grade) {
        element.style.cursor = 'pointer';
        element.style.backgroundImage = 'url("static/images/categories/sc_trainer.png")';
        element.style.backgroundPosition = 'right bottom';
        element.style.backgroundRepeat = 'no-repeat';
        element.style.backgroundSize = '40%';
    }
}

let local_hours_changes = {}

function local_save_hours(e, student_id) {
    $(e).parent().parent().parent().addClass('table-warning')
    local_hours_changes[student_id] = parseFloat(e.value)
}

async function save_hours() {
    if (Object.keys(local_hours_changes).length === 0) return;
    const btn = $('#save-hours-btn')
    btn.addClass('disabled')
    const training_id = btn.attr('data-training-id')

    await fetch(`/api/attendance/mark`, {
        method: 'POST',
        body: JSON.stringify({
            training_id,
            students_hours: local_hours_changes
        })
    });

    $('#grading-modal tr').removeClass('table-warning')
    local_hours_changes = {}
    btn.removeClass('disabled')
}

function make_grades_table(grades) {
    const table = $('<table class="table table-hover">');
    table.append('<thead>')
        .children('thead')
        .append('<tr />')
        .children('tr')
        .append('<th scope="col">Student</th><th scope="col">Email</th><th scope="col">Hours</th>');
    const tbody = table.append('<tbody>').children('tbody');
    grades.forEach(({student_id, full_name, email, hours}) => {
        tbody.append($(`<tr>
                            <td>${full_name}</td>
                            <td>${email}</td>
                            <td style="cursor: pointer"><form onsubmit="return false">
                            <input type="number" min="0" onchange="local_save_hours(this, ${student_id})" value="${hours}" step="0.01"/>
                            </form></td>
                        </tr>`))
    });
    return table;
}

async function open_trainer_modal({event}) {
    if (!event.extendedProps.can_grade) return

    const modal = $('#grading-modal .modal-body');
    modal.empty();
    modal.append($('<div class="spinner-border" role="status"></div>'));
    $('#grading-modal').modal('show');
    const response = await fetch(`/api/attendance/${event.extendedProps.id}/grades`, {
        method: 'GET'
    });
    $('#save-hours-btn').attr('data-training-id', event.extendedProps.id)
    const {group_name, start, grades} = await response.json();
    modal.empty();
    $('#grading-group-name').text(group_name)
    $('#grading-date').text(start.split('T')[0])
    modal.append(make_grades_table(grades));
}

document.addEventListener('DOMContentLoaded', function () {
    let calendarEl = document.getElementById('calendar');

    let calendar = new FullCalendar.Calendar(calendarEl, {
        plugins: ['timeGrid'],
        defaultView: 'timeGridWeek',
        header: {
            left: '',
            center: '',
            // right: '',
            right: 'today, prev, next',
        },
        height: 'auto',
        timeZone: 'Europe/Moscow',
        firstDay: 1,
        allDaySlot: false,
        slotDuration: '00:30:00',
        minTime: '08:00:00',
        maxTime: '21:00:00',
        defaultTimedEventDuration: '01:30',
        eventRender: render,
        datesRender: clearColors,
        eventClick: open_trainer_modal,
        // Event format: yyyy-mm-dd
        events: '/api/calendar/trainings'
    });

    calendar.render();
});
