//Fetch data
function fetchDisciplines() {
    return fetch('/api/sports')
        .then(response => response.json())
        .then(data => data);
}
var disciplines_array = await fetchDisciplines();

//Create array with disciplines(id, name, special)
disciplines_array = disciplines_array["sports"];

//Export disciplines
export default disciplines_array;

//Get HTML elements
var dropdown_disciplines = document.getElementById('disciplinesList');
var disciplines_button = document.getElementById('disciplinesButton');
var drop_down_content_disciplines = document.getElementById('dropDownContentDisciplines');

// Generate options for disciplines dropdown
for (var i = 0; i < disciplines_array.length; i++) {
    var option = document.createElement('li');
    option.textContent = disciplines_array[i].name;
    option.classList.add("drop-down-item");
    dropdown_disciplines.appendChild(option);
    option.addEventListener('click', async function () {
        disciplines_button.textContent = this.textContent;
        drop_down_content_disciplines.classList.toggle('show');
    });
}

// Show/hide dropdown content
disciplines_button.addEventListener('click', function () {
    drop_down_content_disciplines.classList.toggle('show');
});

// Close dropdown content when clicking outside
document.addEventListener('click', function (event) {
    if (!disciplines_button.contains(event.target) &&
        !drop_down_content_disciplines.contains(event.target)) {
        drop_down_content_disciplines.classList.remove('show');
    }
});
