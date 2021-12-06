let students_in_table = {};
let exercises = [];

fetch("/api/fitnesstest/exercises", {
  method: "GET",
  "X-CSRFToken": csrf_token,
})
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    data.forEach((ex, index) => {
      let ex_tab_li = document.createElement("li");
      ex_tab_li.classList.add("nav-item");

      let ex_tab_a = document.createElement("a");
      ex_tab_a.classList.add("nav-link");
      if (index === 0) {
        ex_tab_a.classList.add("active");
      }
      ex_tab_a.innerHTML = ex.name;
      ex_tab_a.setAttribute("href", `#ex-${index}`);
      ex_tab_a.setAttribute("data-toggle", "tab");
      ex_tab_li.appendChild(ex_tab_a);

      document.getElementById("exercise-tabs").appendChild(ex_tab_li);

      let div_table = document.createElement("div");
      div_table.id = `ex-${index}`;
      div_table.classList.add("tab-pane", "fade", "table-responsive");
      if (index === 0) {
          div_table.classList.add("show", "active");
      }

      const student_ex_table = $('<table class="table w-100">');
      student_ex_table
        .append("<thead />")
        .children("thead")
        .append("<tr />")
        .children("tr")
        .append(
          `<th scope="col" width="50%">Student</th><th scope="col">${ex.name}</th>`
        );
        student_ex_table.append(`<tbody id="ex-table-${index}">`);

      div_table.appendChild(student_ex_table[0]);

      document.getElementById("student-exercise-table").appendChild(div_table);
      exercises.push(ex.name);
    });
  })
  .catch(function (err) {
    console.log(err);
  });

function add_student_ex_row(student_id, full_name, email, med_group) {
    let row = null;
    for (let i = 0; i < exercises.length; i++) {
        row = $(`<tr id="student_${student_id}_${i}">
            <td>${full_name} 
            ${med_group === "Special 1" ? `<span class="badge badge-pill badge-danger text-uppercase">${med_group}</span>` : ""}
            </td>
            <td style="cursor: pointer">
                <form onsubmit="return false;">
                    <input class="form-control" type="number" min="0" value="0" step="1"/>
                </form>
            </td>
        </tr>`);
        $(`#ex-table-${i}`).prepend(row);
    }
    students_in_table[student_id] = 1;
}

function parse_student_from_server(data) {
    const [student_id, full_name, email, med_group] = data.split("_");
    const student_row = students_in_table[student_id];
    if (student_row == null) { // check if current student is in the table
        add_student_ex_row(student_id, full_name, email, med_group); // add if student isn't present
    } else {
        // student_row[0].scrollIntoView(); // scroll to the row with student
        // student_row.delay(25).fadeOut().fadeIn().fadeOut().fadeIn();
    }
}

function autocomplete_select(event, ui) {
    event.preventDefault(); // prevent adding the value into the text field
    event.stopPropagation(); // stop other handlers from execution
    $(this).val(""); // clear the input field
    parse_student_from_server(ui.item.value);
}

$(function () {
    $("#student_emails")
        .autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: '/api/attendance/suggest_student',
                    data: {term: request.term},
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

function save_table() {
    const student_ids = Object.keys(students_in_table);
    let res = [];
    for(let i = 0; i < exercises.length; i++) {
        let ex_name = exercises[i];
        student_ids.forEach((sid) => {
            let val = document.getElementById(`student_${sid}_${i}`).getElementsByTagName('input')[0].value;
            console.log(val);
            res.push({student_id: sid, exercise_name: ex_name, value: val});
        });
    }
    fetch("/api/fitnesstest/upload", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf_token,
        },
        body: JSON.stringify({
            result: res
        })
      });
}