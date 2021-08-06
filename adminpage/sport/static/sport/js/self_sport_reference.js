function handleErrors(response) {
    if (!response.ok) {
        const pOkObject = document.getElementById('description-ok');
        const pErrorObject = document.getElementById('description-error');
        pOkObject.classList.add('d-none');
        pErrorObject.classList.remove('d-none');
        console.log("HI");
    }
    return response;
}

async function getStravaActivityInfo(e) {
    const apiUrl = `/api/selfsport/strava_parsing`
    const numberFieldObject = document.getElementById('self-sport-number-input');
    numberFieldObject.placeholder = "Loading...";
    const data = await fetch(`${apiUrl}?${new URLSearchParams({link : e.value})}`)
                    .then(handleErrors)
                    .then(response => response.json());
    numberFieldObject.value = data['hours'];
    numberFieldObject.placeholder = "Number of hours";
    numberFieldObject.removeAttribute('disabled');
}