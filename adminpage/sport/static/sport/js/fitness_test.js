// load semesters
let CURRENT_SEMESTER = null;

function change_semester() {
	const semester_id = $('#fitness-test-semester-choose').val();
	if (semester_id != CURRENT_SEMESTER.value) {
		$("#fitness-test-session-btn").attr('class', 'btn btn-warning w-100 mr-3');
		$('#fitness-test-session-btn').text('Conduct a new retake session');
	} else {
		$("#fitness-test-session-btn").attr('class', 'btn btn-success w-100 mr-3');
		$('#fitness-test-session-btn').text('Conduct a new fitness test session');
	}
	// TODO: change btn href

}

fetch("/api/semesters", { // TODO: Change to the correct link
	method: "GET",
	"X-CSRFToken": csrf_token,
})
	.then((response) => {
		return response.json();
	})
	.then((options) => {
		options.forEach((option, index) => {
			// Assuming the the first coming semester is current semester
			if (index === 0) {
				CURRENT_SEMESTER = option;
			}
			$("#fitness-test-semester-choose").append(
				$(`<option value=${option.value} ${index === 0 ? 'selected': ''}>${option.text}</option>`)
			);
		});
	})
	.catch(function () {
		toastr.error("Error while loading semesters", "Semesters error");
	});

// load sessions
fetch("/api/fitnesstest/sessions", {
	method: "GET",
	"X-CSRFToken": csrf_token,
})
	.then((response) => {
		return response.json();
	})
	.then((data) => {
		data.forEach((session) => {
			let session_row = $(
				// Temporary solution, before was with the django url:
				`<tr style="cursor: pointer" onclick="location.href='${session.id}'">
                    <td>
                        <span class="text-uppercase font-weight-bold">${session.semester.name} ${session.retake ? "Retake" : ""}</span>
                    </td>
                    <td>
                        <span>
                        ${new Date(session.date).toLocaleString("en-GB")}
                        </span>
                    </td>
                    <td>
                        <span class="badge badge-pill badge-light">${session.teacher}</span>
                    </td>
                </tr>`
			);
			$("#ft-session-table-body").prepend(session_row);
		});
	})
	.catch(function (err) {
		console.log(err);
	});
