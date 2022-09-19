fetch('/api/fitnesstest/sessions', {
	method: 'GET',
	'X-CSRFToken': csrf_token,
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
                        <span class="text-uppercase font-weight-bold">${session.semester.name} ${session.retake ? '(retake)' : ''}</span>
                    </td>
                    <td>
                        <span>
                        ${new Date(session.date).toLocaleString('en-GB')}
                        </span>
                    </td>
                    <td>
                        <span class="badge badge-pill badge-light">${session.teacher}</span>
                    </td>
                </tr>`
			);
			$('#ft-session-table-body').prepend(session_row);
		});
	})
	.catch(function (err) {
		console.log(err);
	});
