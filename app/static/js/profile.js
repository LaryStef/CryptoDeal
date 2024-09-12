import "./navbar.js";


const profileDataUrl = new URL("api/profile", origin);
const sessionUrl = new URL("api/sessions", origin);
document.getElementById("set-btn").onclick = openSettingsWindow;
document.getElementById("cancel-set").onclick = closeSettingsWindow;

function loadSessions(clearFirst) {
    fetch(profileDataUrl, {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "X-SCRF-TOKEN": getCookie("access_scrf_token"),
        },
    })
        .then((response) => response.json())
        .then((data) => {
            const sessions = data.userData.sessions;

            let table = document.getElementById("ses-table");

            if (clearFirst) {
                table.innerHTML = `
                    <caption class="sessions-cap">sessions</caption>
                    <tr>
                        <th class="col-head cell">Device</th>
                        <th class="col-head cell">Last activity</th>
                        <th class="cell term-wrap">
                            <button class="term-all" id="term-all">terminate all</button>
                        </th>
                    </tr>`;
            }
            
            sessions.forEach((session) => {
                if (session.isCurrent) {
                    document
                        .getElementById("logout-btn")
                        .setAttribute("sessionId", session.sessionId);

                    table.innerHTML += `<tr>
                        <td class="cell">${session.device}</td>
                        <td class="cell">${session.lastActivity}</td>
                        <td class="cell term-wrap cur-ses">Current</td>
                    </tr>`;
                } else {
                    table.innerHTML += `<tr>
                        <td class="cell">${session.device}</td>
                        <td class="cell">${session.lastActivity}</td>
                        <td class="cell term-wrap">
                            <button class="term-btn" sessionId=${session.sessionId}>terminate</button>
                        </td>
                    </tr>`;
                }
            });
        });
}

document.getElementById("ses-table").addEventListener("click", (event) => {
    if (isTokensRefreshRequired()) {
        refreshTokens();
    }
    if (event.target.classList.contains("term-btn")) {
        
        let sessionId = event.target.attributes.sessionid.value;

        fetch(sessionUrl + "/" + sessionId, {
            method: "DELETE",
            credentials: "same-origin",
            headers: {
                "X-SCRF-TOKEN": getCookie("access_scrf_token"),
            },
        }).then((response) => {
            if (response.status === 200) {
                loadSessions(clearFirst = true);
            }
        });
    } else if (event.target.classList.contains("term-all")) {
        
        fetch(sessionUrl + "/all", {
            method: "DELETE",
            credentials: "same-origin",
            headers: {
                "X-SCRF-TOKEN": getCookie("access_scrf_token"),
            },
        }).then((response) => {
            if (response.status === 200) {
                loadSessions(clearFirst = true);
            }
        });
    }
});

document
    .getElementById("logout-btn")
    .addEventListener("click", () => {
        if (isTokensRefreshRequired()) {
            refreshTokens();
        }

        fetch(sessionUrl + "/my", {
            method: "DELETE",
            credentials: "same-origin",
            headers: {
                "X-SCRF-TOKEN": getCookie("access_scrf_token"),
            },
        }).then((response) => {
            if (response.status === 200) {
                window.location.replace(origin);
            }
        });
    });

function openSettingsWindow() {
    let window = document.getElementById("set-win");
    window.style.transform = "translate(0%)";
    document.getElementById("main-wrap").style.filter = "brightness(0.5)";
    document.getElementById("navbar").style.filter = "brightness(0.5)";
    disableButtons();
}

function closeSettingsWindow() {
    let window = document.getElementById("set-win");
    window.style.transform = "translate(-150%)";
    document.getElementById("main-wrap").style.filter = "brightness(1)";
    document.getElementById("navbar").style.filter = "brightness(1)";
    enableButtons();
}
