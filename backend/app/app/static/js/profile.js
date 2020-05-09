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

async function leave_group(elem, group_id) {
    if (confirm('Are you sure you want to leave this group?')) {
        const response = await sendResults(`/api/unenroll`, {group_id});
        if (response.ok) {
            goto_profile()
        } else {
            alert('unenroll failed')
        }
    }
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
    const table = $(`#hours-modal-${semester_id} .modal-body-table`);
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
    element.style.backgroundColor = get_color(event.title);
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
        return;
    }
    await fetch(`/api/attendance/mark`, {
        method: 'POST',
        body: JSON.stringify({
            training_id,
            students_hours: local_hours_changes
        })
    });

    $('#grading-modal tr').removeClass('table-warning')
    local_hours_changes = {}
    btn.prop('disabled', false);

    hide_alert("hours-alert");
    $('#grading-modal').modal("hide")
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

async function open_trainer_modal({event}) {
    if (!event.extendedProps.can_grade) return

    const modal = $('#grading-modal .modal-body-table');
    modal.empty();
    modal.append($('<div class="spinner-border" role="status"></div>'));
    $('#grading-modal').modal('show');
    const response = await fetch(`/api/attendance/${event.extendedProps.id}/grades`, {
        method: 'GET'
    });
    const save_btn = $('#save-hours-btn');
    save_btn.attr('data-training-id', event.extendedProps.id);
    const {group_name, start, grades} = await response.json();
    modal.empty();
    $('#grading-group-name').text(group_name)
    $('#grading-date').text(start.split('T')[0])
    const duration = event.end - event.start;
    // duration_academic_hours = (duration / 3_600_000) * (60 / 45) = duration / 2_700_000
    current_duration_academic_hours = Math.min(10, round(duration / 2_700_000, 2)) // TODO: hardcoded max = 10 (DB issue)
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
        minTime: '08:00:00',
        maxTime: '21:00:00',
        defaultTimedEventDuration: '01:30',
        eventRender: render,
        eventClick: open_trainer_modal,
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


var app = angular.module("app", ["myDirectives"]);
var myDirectives = angular.module("myDirectives", []);
var boolCheck = 0;
app.controller("UploadController", function ($log) {
this.upload = function () {
  $log.info("Uploading:", this.file || "no file selected!");
}
})


myDirectives.directive("myFileUpload", function ($compile) {
return {
  restrict: "AE",
  require: "ngModel",
  scope: true,
  link: link
};

function link (scope, element, attrs, ngModel) {
var input = angular.element("<input type=\"file\" style=\"display: none;\">");

input.bind("browse", function () {
this.click();
});

input.bind("change", function (changed) {
const file = this.files[0];
const  fileType = file['type'];
const validImageTypes = ['image/gif', 'image/jpeg', 'image/png'];
if (!validImageTypes.includes(fileType)) {
    return window.alert("Wrong format")
}
if (changed.target.files.length < 1) {
  return;
}

var fileName = changed.target.files[0].name;
var reader = new FileReader();

reader.onload = function (loaded) {
scope.fileName = fileName;
ngModel.$setViewValue(loaded.target.result);
boolCheck = 1;
};

reader.readAsDataURL(changed.target.files[0]);
});

$compile(input)(scope);
element.append(input);

scope.browse = function () {
input.triggerHandler("browse");
};

scope.reset = function () {
scope.fileName = null;
ngModel.$setViewValue(null);
boolCheck = 0;
};
scope.check = function () {
if(boolCheck == 0){
  if(ngModel.$viewValue != 1){
      ngModel.$setViewValue(1);
  }
  else{
    ngModel.$setViewValue(0);
  }
}
};
}
});


$(function () {
    $("#student_emails").autocomplete({
        source: "/api/attendance/suggest_student",
        select: autocomplete_select
    });
    $("#student_emails").autocomplete("option", "appendTo", ".student_email_suggestor");
});