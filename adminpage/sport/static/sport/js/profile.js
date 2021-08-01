function make_hours_table(trainings) {
    const table = $('<table class="table table-hover table-sm table-borderless">');
    table.append('<thead>')
        .children('thead')
        .append('<tr />')
        .children('tr')
        .append('<th scope="col">Group</th><th scope="col">Date</th><th scope="col">Hours</th><th scope="col">Approved</th>');
    const tbody = table.append('<tbody>').children('tbody');
    trainings.forEach(({group, custom_name, timestamp, hours, approved}) => {
        tbody.append($(`<tr>
                            <td><span class="badge badge-info text-uppercase">${custom_name || group}</span></td>
                            <td>${timestamp.substr(0, 16)}</td>
                            <td>${hours}</td>
                            <td>${approved === null ? 'Awaiting' : (approved ? 'Yes' : 'No')}</td>
                        </tr>`))
    });
    return table;
}

const loaded_hours = {};

async function fetch_detailed_hours(e) {
    const semester_id = parseInt(e.getAttribute('data-semester-id'), 10);
    if (loaded_hours[semester_id]) return;
    const response = await fetch(`/api/profile/history_with_self/${semester_id}`, {
        method: 'GET',
        "X-CSRFToken": csrf_token,
    });
    const history = await response.json();
    const table = $(`#hours-modal-${semester_id} .modal-body`);
    table.empty();
    console.log(history.trainings)
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

function close_modal(modal_id) {
    $(modal_id).modal('hide');
}

function open_recovered_modal() {
    $('#recovered-modal').modal('show');
    $('#reference-file-input')
        .off('change')
        .val('')
        .on('change', function () {
            const parts = $(this).val().split('\\')
            $(this).prev('.custom-file-label').html(parts[parts.length - 1]);
        })
        .prev('.custom-file-label')
        .html('Reference image');
}

function open_med_group_modal() {
    $('#med-group-modal').modal('show');
}

async function open_selfsport_modal() {
    $('#selfsport-modal').modal('show');
    $('#self-sport-type-help').html('');
    const options = await fetch('/api/selfsport/types')
        .then(res => res.json())
        .then(arr => arr.sort((a, b) => a.name > b.name));
    const el = $('#self-sport-type');
    el.children().remove();
    el.append('<option value="" disabled selected>Select your training type</option>')
    el.off('change').change(function (e) {
        $('#self-sport-type-help').html(options.find(option => option.pk.toString() === e.target.value).application_rule)
    })
    options.forEach(option => {
        el.append(`<option value="${option.pk}">${option.name}</option>`)
    })
}


async function openMedicalInfoModal(groupName, groupDescription) {
    const {data, title, body, footer} = await openModal("#medical-group-info-modal", null);
    title.text(`Medical group info - ${groupName}`);
    body.append(groupDescription)
    footer.html('<div class="container">' +
        '<div class="row justify-content-between">' +
        '<button type="button" class="btn btn-secondary" data-dismiss="modal" onclick="open_med_group_modal()">Change medical group</button> ' +
        '<button type="button" class="btn btn-primary" data-dismiss="modal">Ok</button>' +
        '</div>' +
        '</div>');
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
        let dotEl = info.el.getElementsByClassName('fc-event-dot')[0];
        if (dotEl) {
            dotEl.style.visibility = 'visible';
            dotEl.style.backgroundColor = 'white';
        } else {
            element.style.backgroundImage = 'url("/static/sport/images/categories/sc_trainer.png")';
            element.style.backgroundPosition = 'right bottom';
            element.style.backgroundRepeat = 'no-repeat';
            element.style.backgroundSize = '40%';
        }
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

function add_student_row(student_id, full_name, email, hours, maxHours) {
    const row = $(`<tr id="student_${student_id}">
                    <td class="trainer-table-width show-name-in-trainer-table" onclick="show_email_hide_name()">${full_name}</td>
                    <td class="trainer-table-width hide-email-in-trainer-table" onclick="show_name_hide_email()">${email}</td>
                    <td class="hours-in-trainer-table-right" style="cursor: pointer">
                        <form onsubmit="return false">
                        <div class="btn-group">
                            <a href="#" class="btn btn-outline-primary trainer-editable" onclick="$(this).next().val(0).change()">0</a>
                            <input class="studentHourField form-control trainer-editable" type="number" min="0" max="${current_duration_academic_hours}"
                            onchange="local_save_hours(this, ${student_id})" value="${hours}" step="1"
                            />
                            <a href="#" class="btn btn-outline-primary trainer-editable" onclick="$(this).prev().val(${maxHours}).change()">${maxHours}</a>
                        </div>
                     </form></td>
                </tr>`);
    student_hours_tbody.prepend(row);
    students_in_table[student_id] = row;
}

/* The two functions are applied to the trainer table */
function show_email_hide_name() {
    $('.trainer-table-width.show-name-in-trainer-table').attr('class', 'trainer-table-width hide-name-in-trainer-table');
    $('.trainer-table-width.hide-email-in-trainer-table').attr('class', 'trainer-table-width show-email-in-trainer-table');
}

function show_name_hide_email() {
    $('.trainer-table-width.hide-name-in-trainer-table').attr('class', 'trainer-table-width show-name-in-trainer-table');
    $('.trainer-table-width.show-email-in-trainer-table').attr('class', 'trainer-table-width hide-email-in-trainer-table');
}

/* Return classes back when resizing */
window.addEventListener('resize', function (event) {
    const width = $(window).width()
    const breakpoint = 992

    if (width >= breakpoint) {
        show_name_hide_email()
    }
});


function make_grades_table(grades, maxHours) {
    students_in_table = {};
    const table = $('<table class="table table-hover table-responsive-md">');
    table.append('<thead class="trainer-table-width">')
        .children('thead')
        .append('<tr />')
        .children('tr')
        .append('<th scope="col" class="trainer-table-width show-name-in-trainer-table">Student</th><th scope="col" class="trainer-table-width hide-email-in-trainer-table">Email</th><th scope="col" class="hours-in-trainer-table-right">Hours</th>');
    student_hours_tbody = table.append('<tbody>').children('tbody');
    grades.forEach(({student_id, full_name, email, hours}) => {
        add_student_row(student_id, full_name, email, hours, maxHours);
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

let group_id

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
    const {group_id: gid, group_name, start, grades} = await response.json();
    group_id = gid
    modal.empty();
    $('#grading-group-name').text(group_name)
    $('#grading-date').text(start.split('T')[0])
    const duration = event.end - event.start;
    // duration_academic_hours = (duration / 3_600_000) * (60 / 45) = duration / 2_700_000
    current_duration_academic_hours = Math.min(10, round(duration / 2700000, 2)) // Maximum amount of hours: 10
    const mark_all_btn = $('#put-default-hours-btn');
    mark_all_btn.attr('data-hours', current_duration_academic_hours)
    $('#mark-all-hours-value').text(current_duration_academic_hours)
    modal.append(make_grades_table(grades, current_duration_academic_hours));

    const editable_inputs = $(".trainer-editable");
    save_btn.prop('disabled', !event.extendedProps.can_edit);
    mark_all_btn.prop('disabled', !event.extendedProps.can_edit);
    editable_inputs.prop('disabled', !event.extendedProps.can_edit);
    editable_inputs.toggleClass('disabled', !event.extendedProps.can_edit);

    if (!event.extendedProps.can_edit) {
        show_alert(
            "hours-alert",
            "warning",
            "You can't change this training",
        );
    }
}

document.addEventListener('DOMContentLoaded', function () {
    let calendarEl = document.getElementById('calendar');

    const tabletWidth = 768; // if width is less than this, then week view renders poorly.

    let defaultView = (document.body.clientWidth < tabletWidth) ? 'listWeek' : "timeGridWeek"

    let calendar_settings = {
        // SwipeCalendar
        swipeEffect: 'slide',
        swipeSpeed: 250,

        // FullCalendar
        plugins: ['list', 'timeGrid'],
        defaultView: defaultView,
        titleFormat: {
            month: 'short',
            day: 'numeric'
        },
        header: {
            left: 'timeGridWeek,listWeek',
            center: '',
            right: 'today prev,next',
        },
        height: 'auto',
        timeZone: 'Europe/Moscow',
        firstDay: 1,
        allDaySlot: true,
        slotDuration: '00:30:00',
        minTime: '07:00:00',
        maxTime: '23:00:00',
        eventRender: render,
        eventClick: open_modal,
        // Event format: yyyy-mm-dd
        events: '/api/calendar/trainings'
    }

    let calendar = new SwipeCalendar(calendarEl, calendar_settings);
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
        const maxHours = $('#put-default-hours-btn').attr('data-hours');
        add_student_row(student_id, full_name, email, hours, maxHours); // add if student isn't present
    } else {
        student_row[0].scrollIntoView(); // scroll to the row with student
        student_row.delay(25).fadeOut().fadeIn().fadeOut().fadeIn();
    }
}

async function submit_reference() {
    const formData = new FormData()
    const fileInput = $('#reference-file-input')[0]
    const file = fileInput.files[0]

    if (!file) {
        toastr.error("You can't submit a reference without attaching a file");
        return;
    }

    if (file.size > 10000000) {
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
        toastr.success("Your medical reference was submitted.")
        close_modal('#recovered-modal');
    } catch (error) {
        toastr.error(error.message);
    }
    return false;
}

async function submit_self_sport() {
    const formData = new FormData()

    // // Get file
    // const fileInput = $('#self-sport-file-input')[0];
    // const file = fileInput.files[0];

    // Get link
    const linkInput = $('#self-sport-text-input');
    const link = linkInput.val();

    // Get training_type
    const typeInput = $('#self-sport-type');
    const type = typeInput.val();

    // Get training_type
    const hoursInput = $('#self-sport-number-input');
    const hours = hoursInput.val();

    if (!type) {
        toastr.error("You should select the training type");
        return false;
    }

    if (!link) {
        toastr.error("You should submit a link to your Strava activity");
        return false;
    }

    if (!hours) {
        toastr.error("You should input hours");
        return false;
    }

    // if (file) {
    //     if (file.size > 1E7) {
    //         toastr.error('Image file size too big, expected size <= 10 MB');
    //         return false;
    //     }

    //     try {
    //         const _URL = window.URL || window.webkitURL;
    //         const img = await loadImage(_URL.createObjectURL(file));
    //         if (img.width < 400 || img.width > 4500 || img.height < 400 || img.height > 4500) {
    //             toastr.error('Invalid image width/height, expected them to be in range 400px..4500px');
    //             return false;
    //         }
    //     } catch (e) {
    //         toastr.error('Uploaded file is not an image');
    //         return false;
    //     }

    //     formData.append(fileInput.name, file);
    // }

    if (link) {
        // TODO: regexp for strava
        if (link.startsWith('http://') || link.startsWith('https://')) {
            formData.append(linkInput[0].name, link);
        } else {
            toastr.error("You should submit a link to your Strava activity");
            return false;
        }
    }

    formData.append(typeInput[0].name, type);
    formData.append('hours', hours);

    try {
        await sendResults('/api/selfsport/upload', formData, 'POST', false)
        toastr.success("Your report was successfully uploaded.")
        close_modal('#selfsport-modal');
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
            source: function (request, response) {
                $.ajax({
                    url: '/api/attendance/suggest_student',
                    data: {term: request.term, group_id},
                    dataType: "json",
                    success: response,
                    error: () => response([])
                });
            },
            select: autocomplete_select
        })
        .autocomplete("option", "appendTo", ".student_email_suggestor");
    $('[data-toggle="tooltip"]').tooltip()
});
