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
        method: 'GET',
        "X-CSRFToken": csrf_token,
    });
    const history = await response.json();
    const table = $(`#hours-modal-${semester_id} .modal-body`);
    table.empty();
    table.append(make_hours_table(history.trainings));
    loaded_hours[semester_id] = true;
}

function toggle_ill(elem) {
    if (elem.id === "recovered-btn") {
        open_recovered_modal();
    } else {
        sendResults("/api/profile/sick/toggle", {})
            .then(data => {
                goto_profile();
            })
            .catch(function (error) {
                toastr.error(error.message);
            })
    }
}

function open_recovered_modal() {
    $('#recovered-modal').modal('show');
}

async function openMedicalInfoModal(groupName, groupDescription) {
    const {data, title, body, footer} = await openModal("#medical-group-info-modal", null);
    title.text(`Medical group info - ${groupName}`);
    body.append(`${groupDescription}`)
    footer.html(`
            <div class="container">
                <div class="row justify-content-between">
                    <div><button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button></div>
                </div>
            </div>
        `);
}

/*
    Calendar
*/


function render(info) {
    let element = info.el;
    let event = info.event;

    let props = event.extendedProps;
    element.style.fontSize = "99";
    element.style.backgroundColor = get_color(event.title);
    element.style.cursor = 'pointer';
    if (props.can_grade) {
        element.style.backgroundImage = 'url("/static/sport/images/categories/sc_trainer.png")';
        element.style.backgroundPosition = 'right bottom';
        element.style.backgroundRepeat = 'no-repeat';
        element.style.backgroundSize = '40%';
    }
}

let local_hours_changes = {}

function local_save_hours(e, student_id) {
    e.parentNode.parentNode.parentNode.className = "";
    $(e).parent().parent().parent().addClass('table-warning')
    local_hours_changes[student_id] = parseFloat(e.value)
}

function show_alert(alert_id, level, text = "") {
    const alert_elem = document.getElementById(alert_id);
    alert_elem.className = 'alert alert-' + level;
    alert_elem.textContent = text;
    alert_elem.style.visibility = 'visible';
}

function hide_alert(alert_id) {
    const alert_elem = document.getElementById(alert_id);
    if (alert_elem) {
        alert_elem.textContent = "";
        alert_elem.style.visibility = 'hidden';
    }
}

function parse_local_storage() {
    let parsed = [];
    for (let [key, value] of Object.entries(local_hours_changes)) {
        parsed.push({
            "student_id": key,
            "hours": value,
        })
    }
    return parsed
}

async function save_hours() {
    if (Object.keys(local_hours_changes).length === 0) return;
    const btn = $('#save-hours-btn')
    btn.prop('disabled', true);
    const training_id = btn.attr('data-training-id')

    let hours_valid = true; // Check for validity of hours
    let invalid_row_count = 0;
    let first_invalid_row = null;
    for (const key in local_hours_changes) {
        if (local_hours_changes[key] < 0 || local_hours_changes[key] > current_duration_academic_hours) {
            hours_valid = false;

            const invalid_row_id = "student_" + key.toString();
            const invalid_row = document.getElementById(invalid_row_id); // get row
            if (invalid_row.className.match(/(?:^|\s)table-warning(?!\S)/)) {
                invalid_row.classList.remove("table-warning");
                invalid_row.classList.add("table-danger");
            }
            if (first_invalid_row == null) {
                first_invalid_row = invalid_row;
            }
            invalid_row_count += 1;
        }
    }
    if (!hours_valid) {
        first_invalid_row.scrollIntoView();
        show_alert(
            "hours-alert",
            "danger",
            "Invalid value of hours in " + invalid_row_count.toString() + " row(s)",
        );
    } else {
        await sendResults('/api/attendance/mark', {
            training_id,
            students_hours: parse_local_storage()
        })

        $('#grading-modal tr').removeClass('table-warning')
        local_hours_changes = {}

        hide_alert("hours-alert");
        $('#grading-modal').modal("hide")
    }
    btn.prop('disabled', false);

}

$(document).on('hidden.bs.modal', '#grading-modal', function () {
    hide_alert("hours-alert");
});

function round(num, decimal_places) {
    const decimal = Math.pow(10, decimal_places);
    return Math.round((num + Number.EPSILON) * decimal) / decimal;
}

let student_hours_tbody = null;
let current_duration_academic_hours = 0;
let students_in_table = {}; // <student_id: jquery selector of a row in the table>

function add_student_row(student_id, full_name, email, hours) {
    const row = $(`<tr id="student_${student_id}">
                    <td>${full_name}</td>
                    <td>${email}</td>
                    <td style="cursor: pointer">
                        <form onsubmit="return false">
                            <input class="studentHourField trainer-editable" type="number" min="0" max="${current_duration_academic_hours}" 
                            onchange="local_save_hours(this, ${student_id})" value="${hours}" step="1"
                            />
                     </form></td>
                </tr>`);
    student_hours_tbody.prepend(row);
    students_in_table[student_id] = row;
}

function make_grades_table(grades) {
    students_in_table = {};
    const table = $('<table class="table table-hover table-responsive-md">');
    table.append('<thead>')
        .children('thead')
        .append('<tr />')
        .children('tr')
        .append('<th scope="col">Student</th><th scope="col">Email</th><th scope="col">Hours</th>');
    student_hours_tbody = table.append('<tbody>').children('tbody');
    grades.forEach(({student_id, full_name, email, hours}) => {
        add_student_row(student_id, full_name, email, hours);
    });
    return table;
}

function mark_all(el) {
    const duration_academic_hours = parseFloat($(el).attr('data-hours'))
    $('#grading-modal .modal-body-table input[type=number]').filter(function () {
        return $(this).val() === "0"
    }).val(duration_academic_hours).change();
}


async function open_modal(info) {
    if (info.event.extendedProps.can_grade) {
        return await open_trainer_modal(info)
    }
    return await openGroupInfoModalForStudent(`/api/training/${info.event.extendedProps.id}`)
}

async function open_trainer_modal({event}) {
    const modal = $('#grading-modal .modal-body-table');
    modal.empty();
    modal.append($('<div class="spinner-border" role="status"></div>'));
    $('#grading-modal').modal('show');
    const response = await fetch(`/api/attendance/${event.extendedProps.id}/grades`, {
        method: 'GET',
        "X-CSRFToken": csrf_token,
    });
    const save_btn = $('#save-hours-btn');
    save_btn.attr('data-training-id', event.extendedProps.id);
    const {group_name, start, grades} = await response.json();
    modal.empty();
    $('#grading-group-name').text(group_name)
    $('#grading-date').text(start.split('T')[0])
    const duration = event.end - event.start;
    // duration_academic_hours = (duration / 3_600_000) * (60 / 45) = duration / 2_700_000
    current_duration_academic_hours = Math.min(999.99, round(duration / 2_700_000, 2)) // TODO: hardcoded max = 999.99  (DB issue)
    const mark_all_btn = $('#put-default-hours-btn');
    mark_all_btn.attr('data-hours', current_duration_academic_hours)
    $('#mark-all-hours-value').text(current_duration_academic_hours)
    modal.append(make_grades_table(grades));

    const editable_inputs = $(".trainer-editable");
    save_btn.prop('disabled', !event.extendedProps.can_edit);
    mark_all_btn.prop('disabled', !event.extendedProps.can_edit);
    editable_inputs.prop('disabled', !event.extendedProps.can_edit);

    if (!event.extendedProps.can_edit) {
        show_alert(
            "hours-alert",
            "warning",
            "You can't change this training",
        );
    }
}


document.addEventListener('DOMContentLoaded', function () {
    const tabletWidth = 768; // if width is less than this, then week view renders poorly.
    let calendarEl = document.getElementById('calendar');
    let calendar;
    let calendar_setting = {
        plugins: ['timeGrid'],
        defaultView: 'timeGridWeek',
        header: {
            left: '',
            center: '',
            // right: '',
            right: 'today, prev, next',
        },
        views: {
            timeGridThreeDay: {
                type: 'timeGrid',
                duration: {
                    days: 3
                },
                buttonText: '3 day',
            }
        },
        height: 'auto',
        timeZone: 'Europe/Moscow',
        firstDay: 1,
        allDaySlot: false,
        slotDuration: '00:30:00',
        minTime: '07:00:00',
        maxTime: '23:00:00',
        defaultTimedEventDuration: '01:30',
        eventRender: render,
        eventClick: open_modal,
        windowResize: function (view) {
            // change view on scree rotation
            if (document.body.clientWidth < tabletWidth) {
                calendar.changeView('timeGridThreeDay');
            } else {
                calendar.changeView('timeGridWeek');
            }
        },
        // Event format: yyyy-mm-dd
        events: '/api/calendar/trainings'
    };

    if (document.body.clientWidth < tabletWidth) {
        calendar_setting.defaultView = 'timeGridThreeDay';
        calendar_setting.views.timeGridThreeDay = {
            type: 'timeGrid',
            duration: {days: 3},
            buttonText: '3 day'
        };
    }

    calendar = new FullCalendar.Calendar(calendarEl, calendar_setting);
    calendar.render();
});


function autocomplete_select(event, ui) {
    event.preventDefault(); // prevent adding the value into the text field
    event.stopPropagation(); // stop other handlers from execution
    $(this).val(""); // clear the input field
    const [student_id, full_name, email] = ui.item.value.split("_");
    const hours = 0;
    const student_row = students_in_table[student_id];
    if (student_row == null) { // check if current student is in the table
        add_student_row(student_id, full_name, email, hours); // add if student isn't present
    } else {
        student_row[0].scrollIntoView(); // scroll to the row with student
        student_row.delay(25).fadeOut().fadeIn().fadeOut().fadeIn();
    }
}

async function submit_reference() {
    const formData = new FormData()
    const fileInput = $('#reference-file-input')[0]
    const file = fileInput.files[0]

    toastr.options = {
        positionClass: 'toast-top-center'
    };

    if (file.size > 10_000_000) {
        toastr.error('Image file size too big, expected size <= 10 MB');
        return false;
    }

    try {
        const _URL = window.URL || window.webkitURL;
        const img = await loadImage(_URL.createObjectURL(file));
        if (img.width < 400 || img.width > 4500 || img.height < 400 || img.height > 4500) {
            toastr.error('Invalid image width/height, expected them to be in range 400px..4500px');
            return false;
        }
    } catch (e) {
        toastr.error('Uploaded file is not an image');
        return false;
    }

    formData.append(fileInput.name, file)
    try {
        await sendResults('/api/reference/upload', formData, 'POST', false)
        await sendResults("/api/profile/sick/toggle", {})
        goto_profile()
    } catch (error) {
        toastr.error(error.message);
    }
    return false;
}

$(function () {
    prepareModal('#group-info-modal');
    prepareModal('#medical-group-info-modal');
    $("#student_emails")
        .autocomplete({
            source: "/api/attendance/suggest_student",
            select: autocomplete_select
        })
        .autocomplete("option", "appendTo", ".student_email_suggestor");
    $('[data-toggle="tooltip"]').tooltip()
});