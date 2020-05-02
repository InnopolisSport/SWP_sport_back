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

function enroll(eventClickInfo) {

    let group_id = eventClickInfo.event.extendedProps.id;
    let ans = confirm("Are you sure you want to enroll to group " + eventClickInfo.event.title + "?");
    if (ans) {
        sendResults("/api/enroll", {group_id: group_id})
            .then(data => {
                if (data.ok) {
                    goto_profile();
                } else {
                    switch (data.error.code) {
                        // Not a student account
                        case 3:
                        // Deadline passed
                        case 4:
                            goto_profile();
                            break;
                        //The group is full
                        case 2:
                            eventClickInfo.el.style.backgroundColor = '#ff0000';
                            break;
                    }
                    alert(data.error.description);
                }
            });
    }
}


function render(info) {
    let element = info.el;
    let event = info.event;

    let props = event.extendedProps;
    let available = props.capacity - props.currentLoad;
    element.style.fontSize = "99";
    if (available <= 0) {
        element.style.backgroundColor = "#ff0000"
    } else {
        element.style.backgroundColor = get_color(props.id)
    }

    if (props.training_class) {
        $(element).children(".fc-content").append($(`<div>${props.training_class}</div>`))
    }
}

function showCapacity(mouseEnterInfo) {
    let props = mouseEnterInfo.event.extendedProps;
    mouseEnterInfo.el.title = "Available: " + (props.capacity - props.currentLoad) + " / " + props.capacity;
}

document.addEventListener('DOMContentLoaded', function () {
    let calendarEl = document.getElementById('calendar');

    let calendar = new FullCalendar.Calendar(calendarEl, {
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
        eventClick: enroll,
        eventMouseEnter: showCapacity,
        eventRender: render,
        // Event format: yyyy-mm-dd
        // TODO: at backend use a loop of 10 standard colors as matplotlib do ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        events: '/api/calendar/' + calendarEl.getAttribute('data-sport') + '/schedule'

    });

    calendar.render();
});
