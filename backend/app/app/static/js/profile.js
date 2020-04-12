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