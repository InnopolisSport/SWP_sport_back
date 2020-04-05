async function sendResults(url, data) {
    let response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        // headers: {
        //     // 'Content-Type': 'application/json'
        // }
    });
    return await response.json();
}

function goto_profile() {
    window.location.href = "/profile";
}


function check_empty(list) {
    if (list.childElementCount === 0) {
        const empty_text_node = document.createElement("a");
        empty_text_node.text = "No clubs are available";
        // empty_text_node.href = "#";
        list.appendChild(empty_text_node);
    }
}

function enroll_club(club_id, club_name) {
    const ans = confirm('Are you sure you want to enroll to club ' + club_name + ' ?');
    if (ans) {
        sendResults("/api/enroll", {"group_id": club_id})
            .then(data => {
                if (data.ok) {
                    goto_profile();
                } else {
                    switch (data.error.code) {
                        // Have already been enrolled
                        case 1:
                            goto_profile();
                            break;
                        //The group is full
                        case 2:
                            [...document.getElementsByClassName(club_id)].map(n => n && n.remove());
                            [...document.getElementsByClassName("club-dropdown")].map(n => n && check_empty(n));
                            break;
                    }
                    alert(data.error.description);
                }
            });
    }
}

function enroll_sc(group_id) {
    const ans = confirm('Are you sure you want to enroll to trainings with SC trainers ?');
    if (ans) {
        sendResults("/api/enroll", {"group_id": group_id})
            .then(data => {
                if (data.ok) {
                    goto_profile();
                } else {
                    alert(data.error.description);
                }
            })
    }
}