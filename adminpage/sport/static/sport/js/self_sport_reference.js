let parsed_data;

function handleErrors(response) {
    if (!response.ok) {
        const pOkObject = document.getElementById('description-ok');
        const pErrorObject = document.getElementById('description-error');
        const numberFieldObject = document.getElementById('self-sport-number-input');
        pOkObject.classList.add('d-none');
        pErrorObject.classList.remove('d-none');
        numberFieldObject.placeholder = "Number of hours";
        numberFieldObject.removeAttribute('disabled');
    }
    return response;
}

async function getStravaActivityInfo(e) {
    const apiUrl = `/api/selfsport/strava_parsing`
    const numberFieldObject = document.getElementById('self-sport-number-input');
    numberFieldObject.placeholder = "Loading...";
    parsed_data = await fetch(`${apiUrl}?${new URLSearchParams({link : e.value})}`)
                    .then(handleErrors)
                    .then(response => response.json());
    numberFieldObject.value = parsed_data['hours'];
    numberFieldObject.placeholder = "Number of hours";
    numberFieldObject.removeAttribute('disabled');
}