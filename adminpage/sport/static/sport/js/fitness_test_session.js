const session_id = window.location.href.split('/').pop();

let students_in_table = {};
let exercises = [];
let exercises_map = {};
fetch('/api/fitnesstest/exercises', {
	method: 'GET',
	'X-CSRFToken': csrf_token,
})
	.then((response) => {
		return response.json();
	})
	.then((data) => {
		data.forEach((ex, index) => {
			let ex_tab_li = document.createElement('li');
			ex_tab_li.classList.add('nav-item');

			let ex_tab_a = document.createElement('a');
			ex_tab_a.classList.add('nav-link');
			if (index === 0) {
				ex_tab_a.classList.add('active');
			}
			ex_tab_a.innerHTML = ex.name;
			ex_tab_a.setAttribute('href', `#ex-${index}`);
			ex_tab_a.setAttribute('data-toggle', 'tab');
			ex_tab_li.appendChild(ex_tab_a);

			document.getElementById('exercise-tabs').appendChild(ex_tab_li);

			let div_table = document.createElement('div');
			div_table.id = `ex-${index}`;
			div_table.classList.add('tab-pane', 'fade', 'table-responsive');
			if (index === 0) {
				div_table.classList.add('show', 'active');
			}

			const student_ex_table = $('<table class="table w-100">');
			student_ex_table
				.append('<thead />')
				.children('thead')
				.append('<tr />')
				.children('tr')
				.append(
					`<th scope="col" width="50%">Student</th><th scope="col">${ex.name} — result</th>`
				);
			student_ex_table.append(`<tbody id="ex-table-${index}">`);

			div_table.appendChild(student_ex_table[0]);

			document
				.getElementById('student-exercise-table')
				.appendChild(div_table);
			exercises.push({
				ex_name: ex.name,
				ex_unit: ex.unit,
				ex_select: ex.select,
			});
			exercises_map[ex.name] = index;
		});
		setTimeout(load_session, 10);
	})
	.catch(function (err) {
		console.log(err);
	});

function load_session() {
	if (session_id !== 'new') {
		fetch(`/api/fitnesstest/sessions/${session_id}`, {
			method: 'GET',
			'X-CSRFToken': csrf_token,
		})
			.then((response) => {
				return response.json();
			})
			.then((data) => {
				let ses_data = data['session'];
				let d = new Date(ses_data['date']);
				let mon = d.toLocaleString('en-US', { month: 'short' });
				$('#session-info-date').html(
					`<i>${d.getHours()}:${d.getMinutes()}, ${mon} ${d.getDate()}, ${d.getFullYear()}</i>`
				);
				$('#session-info-teacher').html(ses_data['teacher']);
				let res_data = data['results'];
				for (let i = 0; i < exercises.length; i++) {
					let ex_index = exercises_map[exercises[i].ex_name];
					let student_list = res_data[exercises[i].ex_name];
					for (let j = 0; j < student_list.length; j++) {
						add_student_single_ex_row(
							ex_index,
							student_list[j].student_id,
							student_list[j].student_name,
							student_list[j].student_email,
							student_list[j].student_medical_group
						);
						if (exercises[ex_index].ex_select) {
							$(
								`#ex_${ex_index}_select option[value=${student_list[j].value}]`
							).attr('selected', 'selected');
						} else {
							document
								.getElementById(`ex_${ex_index}_value`)
								.setAttribute(
									'value',
									`${student_list[j].value}`
								);
						}
					}
				}
			})
			.catch(function (err) {
				console.log(err);
			});
	}
}

function add_student_single_ex_row(
	index,
	student_id,
	full_name,
	email,
	med_group
) {
	// Adds single row at particular exercise
	$('#ft-session-save').removeAttr('disabled');
	let row = null;
	console.log("sdad");
	if (exercises[index].ex_select === null) {
		row = $(`<tr id="student_${student_id}_${index}">
                <td>${full_name} 
                ${
					med_group === 'Special 1'
						? `<span class="badge badge-pill badge-danger text-uppercase">${med_group}</span>`
						: ''
				}
                </td>
                <td style="cursor: pointer">
                    <div class="input-group" onsubmit="return false;">
                        <input class="form-control" id="ex_${index}_value"  ${
							exercises[index].ex_unit === 'second(s)'
								? 'type="time" min="00:00:00" value="00:00:00"'
								: 'type="number" min="0" value="0"'
							}"
							step="1"/>
                        ${
							(exercises[index].ex_unit && exercises[index].ex_unit !== 'second(s)')
								? `<div class="input-group-append">
                            <span class="input-group-text">${exercises[index].ex_unit}</span>
                            </div>`
								: ''
						}
                    </div>
                </td>
            </tr>`);
	} else {
		row = $(`<tr id="student_${student_id}_${index}">
                <td>${full_name} 
                ${
					med_group === 'Special 1'
						? `<span class="badge badge-pill badge-danger text-uppercase">${med_group}</span>`
						: ''
				}
                </td>
                <td style="cursor: pointer">
                    <select class="custom-select" id="ex_${index}_select">
                        <option selected disabled value="-1">Choose...</option>
                    </select>
                </td>
            </tr>`);
	}
	$(`#ex-table-${index}`).prepend(row);
	if (exercises[index].ex_select !== null) {
		for (let j = 0; j < exercises[index].ex_select.length; j++) {
			let option = document.createElement('option');
			option.setAttribute('value', `${j}`);
			option.innerHTML = exercises[index].ex_select[j];
			$(`#ex_${index}_select`).first().append(option);
		}
	}
	students_in_table[student_id] = 1;
}

function add_student_ex_row(student_id, full_name, email, med_group) {
	// Adds multiple rows i.e., at each exercise
	$('#ft-session-save').removeAttr('disabled');
	let row = null;
	for (let i = 0; i < exercises.length; i++) {
		if (exercises[i].ex_select === null) {
			row = $(`<tr id="student_${student_id}_${i}">
                <td>${full_name} 
                ${
					med_group === 'Special 1'
						? `<span class="badge badge-pill badge-danger text-uppercase">${med_group}</span>`
						: ''
				}
                </td>
                <td style="cursor: pointer">
                    <div class="input-group" onsubmit="return false;">
                        <input class="form-control" id="ex_${i}_value" ${
							exercises[i].ex_unit === 'second(s)'
								? 'type="time" min="00:00:00" value="00:00:00"'
								: 'type="number" min="0" value="0"'
							}"
						step="1"/>
                        ${
							(exercises[i].ex_unit && exercises[i].ex_unit !== 'second(s)')
								? `<div class="input-group-append">
                            <span class="input-group-text">${exercises[i].ex_unit}</span>
                            </div>`
								: ''
						}
                    </div>
                </td>
            </tr>`);
		} else {
			row = $(`<tr id="student_${student_id}_${i}">
                <td>${full_name} 
                ${
					med_group === 'Special 1'
						? `<span class="badge badge-pill badge-danger text-uppercase">${med_group}</span>`
						: ''
				}
                </td>
                <td style="cursor: pointer">
                    <select class="custom-select" id="ex_${i}_select">
                        <option selected disabled value="-1">Choose...</option>
                    </select>
                </td>
            </tr>`);
		}
		$(`#ex-table-${i}`).prepend(row);
		if (exercises[i].ex_select !== null) {
			for (let j = 0; j < exercises[i].ex_select.length; j++) {
				let option = document.createElement('option');
				option.setAttribute('value', `${j}`);
				option.innerHTML = exercises[i].ex_select[j];
				$(`#ex_${i}_select`).first().append(option);
			}
		}
	}
	students_in_table[student_id] = 1;
}

let current_student;

function parse_student_from_server(data) {
	const [student_id, full_name, email, med_group, gender] = data.split('_');
	current_student = parseInt(student_id);
	const student_row = students_in_table[student_id];
	if (student_row == null) {
		// check if current student is in the table
		if (gender === '-1') {
			$('#gender-modal-name').text(full_name);
			$('#gender-modal').modal('show');
		}
		add_student_ex_row(student_id, full_name, email, med_group); // add if student isn't present
	} else {
		// student_row[0].scrollIntoView(); // scroll to the row with student
		// student_row.delay(25).fadeOut().fadeIn().fadeOut().fadeIn();
	}
}

function autocomplete_select(event, ui) {
	event.preventDefault(); // prevent adding the value into the text field
	event.stopPropagation(); // stop other handlers from execution
	$(this).val(''); // clear the input field
	parse_student_from_server(ui.item.value);
}

$(function () {
	$('#student_emails')
		.autocomplete({
			source: function (request, response) {
				$.ajax({
					url: '/api/fitnesstest/suggest_student',
					data: { term: request.term },
					dataType: 'json',
					success: response,
					error: () => response([]),
				});
			},
			select: autocomplete_select,
		})
		.autocomplete('option', 'appendTo', '.student_email_suggestor');
	$('[data-toggle="tooltip"]').tooltip();
});

function save_table() {
	const student_ids = Object.keys(students_in_table);
	let res = [];
	let cant_submit = false;
	for (let i = 0; i < exercises.length; i++) {
		if (student_ids.length === 0) {
			cant_submit = true;
			break;
		}
		let ex_name = exercises[i].ex_name;
		student_ids.forEach((sid) => {
			let val;
			let inp_field = document
				.getElementById(`student_${sid}_${i}`)
				.getElementsByTagName('input')[0];
			let sel_field = document
				.getElementById(`student_${sid}_${i}`)
				.getElementsByTagName('select')[0];
			if (inp_field) {
				if (exercises[i]["ex_unit"] === 'second(s)') {
					val = inp_field.value.split(':').reduce((acc, time) => (60 * acc) + +time);
				} else {
					val = inp_field.value;
				}
			} else {
				val = sel_field.value;
			}
			if (val === '') {
				toastr.error(
					`There are no values for some students in <b>${ex_name} exercise</b>`,
					'Value error'
				);
				cant_submit = true;
			} else if (parseInt(val) < 0) {
				toastr.error(
					`Values should be <b>positive</b> or you have not selected the option. Check <b>${ex_name} exercise</b>`,
					'Value error'
				);
				cant_submit = true;
			}
			res.push({ student_id: sid, exercise_name: ex_name, value: val });
		});
	}
	if (cant_submit) {
		return;
	}
	if (session_id === 'new') {
		fetch('/api/fitnesstest/upload', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrf_token,
			},
			body: JSON.stringify({
				result: res,
			}),
		})
			.then((response) => {
				if (response.ok) {
					return response.json();
				}
				throw new Error('Something went wrong.');
			})
			.then((response) => {
				$('#ft-session-save').attr('disabled', '');
				toastr.success(
					'The fitness test has been successfuly saved',
					'Saved',
					1500
				);
				setTimeout(() => {
					window.location.href = `/fitness_test/${response['session_id']}`;
				}, 1500);
			})
			.catch(function (error) {
				toastr.error(`${error}`, 'Server error');
			});
	} else {
		fetch(`/api/fitnesstest/upload/${session_id}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrf_token,
			},
			body: JSON.stringify({
				result: res,
			}),
		})
			.then((response) => {
				if (response.ok) {
					return response.json();
				}
				throw new Error('Something went wrong.');
			})
			.then(() => {
				toastr.success(
					'The fitness test has been successfuly saved',
					'Saved',
					1500
				);
			})
			.catch(function (error) {
				toastr.error(`${error}`, 'Server error');
			});
	}
}

function save_gender(val) {
	fetch('/api/profile/change_gender', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrf_token,
		},
		body: JSON.stringify({ student_id: current_student, gender: val }),
	})
		.then((response) => {
			if (response.ok) {
				return response.text();
			}
			throw new Error('Something went wrong.');
		})
		.then(() => {
			toastr.success('The gender has been successfuly set', 'Set', 1000);
			$('#gender-modal').modal('hide');
		})
		.catch(function (error) {
			toastr.error(`${error}`, 'Server error');
		});
}
