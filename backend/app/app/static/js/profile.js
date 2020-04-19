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