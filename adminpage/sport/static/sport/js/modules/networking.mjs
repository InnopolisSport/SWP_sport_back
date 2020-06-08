class ApiError extends Error {
    constructor(message, code, status) {
        super(message);
        this.code = code;
        this.status = status;
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrf_token = getCookie('csrftoken');

async function sendResults(url, data, method = 'POST') {
    function handleError(response) {
        if (!response.ok) {
            return response.json()
                .then(data => {
                    throw new ApiError(
                        data.detail,
                        data.code,
                        response.status
                    );
                });

        }
        return response.json();
    }

    let response = await fetch(url, {
        method: method,
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf_token,
        },
    }).then(handleError);
}

function goto_profile() {
    window.location.href = "/django/profile";
}

function reload_page() {
    window.location.reload();
}