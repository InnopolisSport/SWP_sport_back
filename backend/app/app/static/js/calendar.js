// let f = require("@fullcalendar/core");
// let d = require("@fullcalendar/daygrid");
// let t = require("@fullcalendar/timegrid");

function getMonday(d) {
    d = new Date(d);
    let day = d.getDay(),
        diff = d.getDate() - day + (day === 0 ? -6 : 1); // adjust when day is sunday
    return new Date(d.setDate(diff))
}

function sendResults(url, data) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(
        JSON.stringify(data)
    );
}

function enroll(eventClickInfo) {
    let ans = confirm("Are you sure you want to enroll to " + eventClickInfo.event.title + "?");
    if (ans) {
        sendResults("/enroll", {group_id: 4});
    }
}

function showCapacity(mouseEnterInfo) {
    let props = mouseEnterInfo.event.extendedProps;
    mouseEnterInfo.el.title = "Available: " + (props.capacity - props.currentLoad) + " / " + props.capacity;
    mouseEnterInfo.el.showTip();
}

document.addEventListener('DOMContentLoaded', function () {
    let calendarEl = document.getElementById('calendar');

    let calendar = new FullCalendar.Calendar(calendarEl, {
        plugins: ['timeGrid'],
        defaultView: 'timeGridWeek',
        header: {
            left: '',
            center: 'title',
            right: ''
        },
        height: 'auto',
        timeZone: 'Europe/Moscow',
        firstDay: 1,
        allDaySlot: false,
        slotDuration: '00:45:00',
        minTime: '08:30:00',
        maxTime: '21:00:00',
        defaultTimedEventDuration: '01:30',
        eventClick: enroll,
        eventMouseEnter: showCapacity,
        // Event format: yyyy-mm-dd
        // TODO: create backend for calendar Consider https://fullcalendar.io/docs/events-json-feed
        // TODO: at backend use a loop of 10 standard colors as matplotlib do ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        eventSources: [

            // your event source
            {
                events: [ // put the array in the `events` property
                    {
                        title: 'G1',
                        start: '2020-03-26T08:30:00',
                        end: '2020-03-26T10:00:00',
                        capacity: 35,
                        currentLoad: 5
                    }
                ]
            },

            {
                events: [ // put the array in the `events` property
                    {
                        title: 'G2',
                        start: '2020-03-26T09:15:00',
                        end: '2020-03-26T10:45:00',
                        capacity: 45,
                        currentLoad: 0
                    }
                ]
            }

            // any other event sources...

        ],
        // maxTime: "20:00:00",
    });

    calendar.render();
});
