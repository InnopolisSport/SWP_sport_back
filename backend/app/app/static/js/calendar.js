// let f = require("@fullcalendar/core");
// let d = require("@fullcalendar/daygrid");
// let t = require("@fullcalendar/timegrid");

function sendResults(url, data) {
    fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            // 'Content-Type': 'application/json'
        }
    });
}

function enroll(eventClickInfo) {
    let group_id = eventClickInfo.event.extendedProps.id;
    let ans = confirm("Are you sure you want to enroll to Group " + group_id + "?");
    if (ans) {
        sendResults("/api/enroll", {group_id: group_id});
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
        slotDuration: '00:45:00',
        minTime: '08:30:00',
        maxTime: '21:00:00',
        defaultTimedEventDuration: '01:30',
        eventClick: enroll,
        eventMouseEnter: showCapacity,
        // Event format: yyyy-mm-dd
        // TODO: at backend use a loop of 10 standard colors as matplotlib do ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        events: '/api/calendar/' + calendarEl.getAttribute('data-sport') + '/schedule'
        // eventSources: [
        //
        //     // your event source
        //     {
        //         events: [ // put the array in the `events` property
        //             {
        //                 title: 'G1',
        //                 start: '2020-03-26T08:30:00',
        //                 end: '2020-03-26T10:00:00',
        //                 capacity: 35,
        //                 currentLoad: 5,
        //                 group_id: 1
        //             }
        //         ]
        //     },
        //
        //     {
        //         events: [ // put the array in the `events` property
        //             {
        //                 title: 'G2',
        //                 start: '2020-03-26T09:15:00',
        //                 end: '2020-03-26T10:45:00',
        //                 capacity: 45,
        //                 currentLoad: 0,
        //                 group_id: 2
        //             }
        //         ]
        //     }
        //
        //     // any other event sources...
        //
        // ],
    });

    calendar.render();
});
