const origin = location.origin;

const loginUrl = new URL("api/auth/sign-in", origin);
const registerUrl = new URL("api/auth/register/apply", origin);
const newCodeUrl = new URL("api/auth/register/new-code", origin);
const verifyCodeUrl = new URL("api/auth/register/verify", origin);
const restoreUrl = new URL("api/auth/restore/apply", origin);
const restoreNewCodeUrl = new URL("api/auth/restore/new-code", origin);
const restoreVerifyUrl = new URL("api/auth/restore/verify", origin);
const refreshTokensUrl = new URL("api/auth/refresh-tokens", origin);
const profileDataUrl = new URL("api/profile", origin);
const sessionUrl = new URL("api/sessions", origin);

const cooldown = 30;
const cooldownRec = 30;

function getDeviceData() {
    let browser = "unknown browser";
    let os = "unknown os";
    let osVersion = "";

    let userAgent = navigator.userAgent;

    if (userAgent.indexOf("Edg") > -1) {
        browser = "Microsoft Edge";
    } else if (userAgent.indexOf("Chrome") > -1) {
        browser = "Chrome";
    } else if (userAgent.indexOf("Firefox") > -1) {
        browser = "Firefox";
    } else if (userAgent.indexOf("Safari") > -1) {
        browser = "Safari";
    } else if (userAgent.indexOf("Opera") > -1) {
        browser = "Opera";
    } else if (
        userAgent.indexOf("Trident") > -1 ||
        userAgent.indexOf("MSIE") > -1
    ) {
        browser = "Internet Explorer";
    }

    const clientStrings = [
        {s: "Windows 10", r: /(Windows 10.0|Windows NT 10.0)/},
        {s: "Windows 8.1", r: /(Windows 8.1|Windows NT 6.3)/},
        {s: "Windows 8", r: /(Windows 8|Windows NT 6.2)/},
        {s: "Windows 7", r: /(Windows 7|Windows NT 6.1)/},
        {s: "Windows Vista", r: /Windows NT 6.0/},
        {s: "Windows Server 2003", r: /Windows NT 5.2/},
        {s: "Windows XP", r: /(Windows NT 5.1|Windows XP)/},
        {s: "Windows 2000", r: /(Windows NT 5.0|Windows 2000)/},
        {s: "Windows ME", r: /(Win 9x 4.90|Windows ME)/},
        {s: "Windows 98", r: /(Windows 98|Win98)/},
        {s: "Windows 95", r: /(Windows 95|Win95|Windows_95)/},
        {s: "Windows NT 4.0", r: /(Windows NT 4.0|WinNT4.0|WinNT|Windows NT)/},
        {s: "Windows CE", r: /Windows CE/},
        {s: "Windows 3.11", r: /Win16/},
        {s: "Android", r: /Android/},
        {s: "Open BSD", r: /OpenBSD/},
        {s: "Sun OS", r: /SunOS/},
        {s: "Chrome OS", r: /CrOS/},
        {s: "Linux", r: /(Linux|X11(?!.*CrOS))/},
        {s: "iOS", r: /(iPhone|iPad|iPod)/},
        {s: "Mac OS X", r: /Mac OS X/},
        {s: "Mac OS", r: /(Mac OS|MacPPC|MacIntel|Mac_PowerPC|Macintosh)/},
        {s: "QNX", r: /QNX/},
        {s: "UNIX", r: /UNIX/},
        {s: "BeOS", r: /BeOS/},
        {s: "OS/2", r: /OS\/2/},
        {
            s: "Search Bot",
            r: /(nuhk|Googlebot|Yammybot|Openbot|Slurp|MSNBot|Ask Jeeves\/Teoma|ia_archiver)/,
        },
    ];
    for (let id in clientStrings) {
        let cs = clientStrings[id];
        if (cs.r.test(userAgent)) {
            os = cs.s;
            break;
        }
    }

    if (/Windows/.test(os)) {
        osVersion = /Windows (.*)/.exec(os)[1];
        os = "Windows";
    }

    switch (os) {
        case "Mac OS":
        case "Mac OS X":
        case "Android":
            osVersion =
                /(?:Android|Mac OS|Mac OS X|MacPPC|MacIntel|Mac_PowerPC|Macintosh) ([\.\_\d]+)/.exec(
                    userAgent
                )[1];
            break;

        case "iOS":
            osVersion = /OS (\d+)_(\d+)_?(\d+)?/.exec(nVer);
            osVersion =
                osVersion[1] + "." + osVersion[2] + "." + (osVersion[3] | 0);
            break;
    }

    return browser + ", " + os + osVersion;
}

if (isTokensRefreshRequired()) {
    refreshTokens();
} else {
    loadProfile();
}

async function refreshTokens() {
    let response = await fetch(refreshTokensUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-SCRF-TOKEN": getCookie("refresh_scrf_token"),
            Device: getDeviceData(),
        },
    });

    if (response.status === 200) {
        loadProfile();
    }
}

function isTokensRefreshRequired() {
    let access = getCookie("access_token");

    if (
        access != "" &&
        Math.floor(Date.now() / 1000) <
            Number(JSON.parse(atob(access.split(".")[1])).exp) - 1
    ) {
        return false;
    }
    return true;
}

function getCookie(cookie) {
    cookie += "=";
    let cookies = document.cookie.split("; ");
    let token = "";

    cookies.forEach((element) => {
        if (element.substring(0, cookie.length) === cookie) {
            token = element.substring(cookie.length, element.length);
        }
    });
    return token;
}

function loadProfile() {
    loadSessions(false);

    let authClasses = document.getElementById("auth-button").classList;
    let profileClasses = document.getElementById("profile-button").classList;
    if (
        !authClasses.contains("display-off") &&
        profileClasses.contains("display-off")
    ) {
        authClasses.add("display-off");
        profileClasses.remove("display-off");
    }

    let access = getCookie("access_token");
    let payload = JSON.parse(atob(access.split(".")[1]));

    document.getElementById("name").innerText = payload.name;
    document.getElementById("username").innerText = payload.name;

    const avatarUrl = new URL(
        `/static/png/Alien${payload.alien_number}.png`,
        location.origin
    );
    document.getElementById("avatar").src = avatarUrl;
    document.getElementById("main-avatar").src = avatarUrl;
}

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

document.getElementById("left-switch").onclick = leftSwitchTransform;
document.getElementById("right-switch").onclick = rightSwitchTransform;
document.getElementById("sign-up").onclick = openSignUpWindow;
document.getElementById("sign-in").onclick = openSignInWindow;
document.getElementById("set-btn").onclick = openSettingsWindow;

document.getElementById("dropdown-sign-in").onclick = openSignInWindow;
document.getElementById("dropdown-sign-up").onclick = openSignUpWindow;

document.getElementById("cancel").onclick = closeLoginWindow;
document.getElementById("mail-cancel").onclick = closeConfirmWindow;
document.getElementById("email-cancel").onclick = closeEmailWindow;
document.getElementById("mail-cancel-rec").onclick = closePasswordWindow;
document.getElementById("cancel-set").onclick = closeSettingsWindow;

document.getElementById("code-btn").onclick = sendNewCode;
document.getElementById("code-btn-rec").onclick = sendNewCodeRec;

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

document
    .getElementById("login-form-id")
    .addEventListener("submit", async (e) => {
        e.preventDefault();

        let formData = new FormData(document.getElementById("login-form-id"));

        let response = await fetch(loginUrl, {
            method: "POST",
            credentials: "same-origin",
            body: formData,
            headers: {
                Device: getDeviceData(),
            },
        });

        if (response.status === 200) {
            closeLoginWindow();
            loadProfile();
        } else {
            let error = await response.json();
            document.getElementById("login-info").innerHTML =
                error["error"]["message"];
        }
    });

document
    .getElementById("register-form-id")
    .addEventListener("submit", async (e) => {
        e.preventDefault();

        let formData = new FormData(
            document.getElementById("register-form-id")
        );

        if (validateRegisterData(formData)) {
            let response = await fetch(registerUrl, {
                method: "POST",
                credentials: "same-origin",
                body: formData,
            });

            if (response.status === 201) {
                if (isTimerGoing) {
                    disableTimer(timerId);
                }

                sessionStorage.setItem(
                    "request_id",
                    response.headers.get("Request-Id")
                );

                document
                    .getElementById("get-code-wrapper")
                    .classList.add("display-off");
                document
                    .getElementById("new-code")
                    .classList.remove("display-off");
                document.getElementById("input-code").style.backgroundColor =
                    "#7d42e7";
                document.getElementById("input-code").value = "";
                timerId = showTime(cooldown);

                let email = document.getElementById("email-input").value;
                sessionStorage.setItem("email-reg", email);
                closeLoginWindow();
                openConfirmWindow(email);
            } else {
                error = await response.json();
                document.getElementById("register-info").innerHTML =
                    error["error"]["message"];
            }
        }
    });

function disableButtons() {
    document.getElementsByClassName("auth-link")[0].disabled = true;
    document.getElementsByClassName("auth-link")[1].disabled = true;
}

function enableButtons() {
    document.getElementsByClassName("auth-link")[0].disabled = false;
    document.getElementsByClassName("auth-link")[1].disabled = false;
}

function leftSwitchTransform() {
    document.getElementById("mode-light").style.transform = "translate(0%)";
    if (window.innerWidth <= 650) {
        document.getElementById("register-container").style.transform =
            "translate(-100%)";
        document.getElementById("login-container").style.transform =
            "translate(0%, -100%)";
    } else if (window.innerWidth <= 1000) {
        document.getElementById("register-container").style.transform =
            "translate(-100%)";
        document.getElementById("login-container").style.transform =
            "translate(5%, -100%)";
    } else {
        document.getElementById("register-container").style.transform =
            "translate(-100%)";
        document.getElementById("login-container").style.transform =
            "translate(50%, -100%)";
    }
}

function rightSwitchTransform() {
    document.getElementById("mode-light").style.transform = "translate(100%)";
    if (window.innerWidth <= 650) {
        document.getElementById("register-container").style.transform =
            "translate(0%)";
        document.getElementById("login-container").style.transform =
            "translate(100%, -100%)";
    } else if (window.innerWidth <= 1000) {
        document.getElementById("register-container").style.transform =
            "translate(5%)";
        document.getElementById("login-container").style.transform =
            "translate(200%, -100%)";
    } else {
        document.getElementById("register-container").style.transform =
            "translate(50%)";
        document.getElementById("login-container").style.transform =
            "translate(200%, -100%)";
    }
}

function rightSwitch() {
    document.getElementById("mode-light").classList.add("transition-off");
    document
        .getElementById("register-container")
        .classList.add("transition-off");
    document.getElementById("login-container").classList.add("transition-off");

    rightSwitchTransform();
    setTimeout(() => {
        document
            .getElementById("mode-light")
            .classList.remove("transition-off");
        document
            .getElementById("register-container")
            .classList.remove("transition-off");
        document
            .getElementById("login-container")
            .classList.remove("transition-off");
    }, 400);
}

function leftSwitch() {
    document.getElementById("mode-light").classList.add("transition-off");
    document
        .getElementById("register-container")
        .classList.add("transition-off");
    document.getElementById("login-container").classList.add("transition-off");

    leftSwitchTransform();
    setTimeout(() => {
        document
            .getElementById("mode-light")
            .classList.remove("transition-off");
        document
            .getElementById("register-container")
            .classList.remove("transition-off");
        document
            .getElementById("login-container")
            .classList.remove("transition-off");
    }, 400);
}

function openSignInWindow() {
    leftSwitch();
    let loginWindow = document.getElementById("login");
    loginWindow.style.opacity = 1;
    if (window.innerWidth <= 650) {
        loginWindow.style.transform = "translate(0%, 30%)";
    } else {
        loginWindow.style.transform = "translate(50%, 30%)";
    }
    document.getElementById("main-wrap").style.filter = "brightness(0.5)";
    document.getElementById("navbar").style.filter = "brightness(0.5)";
    disableButtons();
}

function openSignUpWindow() {
    rightSwitch();
    let loginWindow = document.getElementById("login");
    loginWindow.style.opacity = 1;
    if (window.innerWidth <= 650) {
        loginWindow.style.transform = "translate(0%, 30%)";
    } else {
        loginWindow.style.transform = "translate(50%, 30%)";
    }
    document.getElementById("main-wrap").style.filter = "brightness(0.5)";
    document.getElementById("navbar").style.filter = "brightness(0.5)";
    disableButtons();
}

function closeLoginWindow() {
    let loginWindow = document.getElementById("login");
    loginWindow.style.opacity = 0;
    loginWindow.style.transform = "translate(-100%, 30%)";
    document.getElementById("main-wrap").style.filter = "brightness(1)";
    document.getElementById("navbar").style.filter = "brightness(1)";
    document.getElementById("login-info").innerText = "";
    document.getElementById("register-info").innerText = "";
    enableButtons();
}

document.onkeydown = function (evt) {
    let isEscape = false;
    if ("key" in evt) {
        isEscape = evt.key === "Escape" || evt.key === "Esc";
    } else {
        isEscape = evt.keyCode === 27;
    }
    if (isEscape) {
        closeLoginWindow();
    }
};

function openConfirmWindow(email) {
    document.getElementById("email").innerText = email;
    let window = document.getElementById("confirm-window");
    window.style.opacity = 1;
    window.style.transform = "translate(0%)";
    window.style.visibility = "visible";

    document.getElementById("main-wrap").style.filter = "brightness(0.5)";
    document.getElementById("navbar").style.filter = "brightness(0.5)";
    disableButtons();
}

function closeConfirmWindow() {
    let window = document.getElementById("confirm-window");
    window.style.opacity = 0;
    window.style.transform = "translate(200%)";
    document.getElementById("main-wrap").style.filter = "brightness(1)";
    document.getElementById("navbar").style.filter = "brightness(1)";
    document.getElementById("input-code").style.backgroundColor = "#7d42e7";
    document.getElementById("input-code").value = "";

    setTimeout(() => {
        window.style.visibility = "hidden";
    }, 400);
    enableButtons();
    if (isTimerGoing) {
        disableTimer(timerId);
    }
}

document.addEventListener("input", () => {
    let field = document.getElementById("input-code");
    if (field.value.length === 6) {
        verifyCode();
    }
});

let timerId;
let isTimerGoing = false;

function showTime(duration) {
    isTimerGoing = true;
    let minutes = Math.floor(duration / 60);
    let seconds = duration % 60;
    timerId = setInterval(() => {
        let time;
        if (seconds < 10) {
            time = `${minutes}:0${seconds}`;
        } else {
            time = `${minutes}:${seconds}`;
        }
        document.getElementById("code-time").innerHTML = time;
        if (seconds != 0) {
            seconds -= 1;
        } else {
            minutes -= 1;
            seconds = 59;
        }
    }, 1000);

    let thisTimerId = timerId;
    setTimeout(() => {
        if (thisTimerId == timerId) {
            disableTimer(timerId);
            document.getElementById("new-code").classList.add("display-off");
            document
                .getElementById("get-code-wrapper")
                .classList.remove("display-off");
        }
    }, (duration + 1) * 1000);

    return timerId;
}

function disableTimer(timerID) {
    clearInterval(timerID);
    isTimerGoing = false;
}

async function verifyCode() {
    let data = new Map();
    data.set("code", document.getElementById("input-code").value);

    response = await fetch(verifyCodeUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "Request-Id": sessionStorage.getItem("request_id"),
            Device: getDeviceData(),
        },
        body: JSON.stringify(Object.fromEntries(data)),
    });

    if (response.status == 200) {
        closeConfirmWindow();
        loadProfile();
    } else {
        document.getElementById("input-code").style.backgroundColor = "#BF1A3E";
    }
}

async function sendNewCode() {
    let data = new Map();
    data.set("email", sessionStorage.getItem("email-reg"));

    response = await fetch(newCodeUrl, {
        method: "PATCH",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "Request-Id": sessionStorage.getItem("request_id"),
        },
        body: JSON.stringify(Object.fromEntries(data)),
    });

    if (response.status == 200) {
        document
            .getElementById("get-code-wrapper")
            .classList.add("display-off");
        document.getElementById("new-code").classList.remove("display-off");
        document.getElementById("input-code").style.backgroundColor = "#7d42e7";
        document.getElementById("input-code").value = "";
        timerId = showTime(cooldown);
    }
}

function validateRegisterData(formData) {
    const re =
        /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;

    let username = formData.get("username");
    let pass = formData.get("password");
    let email = formData.get("email");

    if (username.length < 6 || username.length > 20) {
        document.getElementById("register-info").innerText =
            "username length must be between 6 and 20";
        return false;
    }
    if (username.includes(" ")) {
        document.getElementById("register-info").innerText =
            "username can't include any spaces";
        return false;
    }
    if (pass.length < 6 || pass.length > 20) {
        document.getElementById("register-info").innerText =
            "password length must be between 6 and 20";
        return false;
    }
    if (pass.includes(" ")) {
        document.getElementById("register-info").innerText =
            "password can't include any spaces";
        return false;
    }
    if (!re.test(email)) {
        document.getElementById("register-info").innerText = "invalid email";
        return false;
    }

    return true;
}

document.getElementById("recovery-btn").addEventListener("click", () => {
    closeLoginWindow();
    openEmailWindow();
});

document.getElementById("email-submit").addEventListener("click", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email-input-recovery").value;
    sessionStorage.setItem("email-rec", email);

    let data = new Map();
    data.set("email", email);

    let response = await fetch(restoreUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(Object.fromEntries(data)),
    });

    if (response.status === 201) {
        closeEmailWindow();
        openPasswordWindow(email);
        if (isTimerGoingRec) {
            disableTimerRec(timerIdRec);
        }

        document
            .getElementById("get-code-wrapper-rec")
            .classList.add("display-off");
        document.getElementById("new-code-rec").classList.remove("display-off");
        timerIdRec = showTimeRec(cooldownRec);

        sessionStorage.setItem(
            "request_id",
            response.headers.get("Request-Id")
        );
    } else if (response.status === 404 || response.status === 425) {
        let error = await response.json();
        document.getElementById("pass-info").innerText =
            error["error"]["message"];
    }
});

function openEmailWindow() {
    let window = document.getElementById("email-window");
    window.style.opacity = 1;
    window.style.transform = "translate(0%)";
    window.style.visibility = "visible";

    document.getElementById("main-wrap").style.filter = "brightness(0.5)";
    document.getElementById("navbar").style.filter = "brightness(0.5)";
    disableButtons();
}

function closeEmailWindow() {
    let window = document.getElementById("email-window");
    window.style.opacity = 0;
    window.style.transform = "translate(-200%)";
    document.getElementById("main-wrap").style.filter = "brightness(1)";
    document.getElementById("navbar").style.filter = "brightness(1)";
    document.getElementById("email-input-recovery").value = "";
    document.getElementById("pass-info").innerText = "";

    setTimeout(() => {
        window.style.visibility = "hidden";
        window.style.transition = "none";
        window.style.transform = "translate(200%)";
        window.style.transition =
            "all var(--login-transition-duration) ease-out";
    }, 400);

    enableButtons();
}

async function sendNewCodeRec() {
    let data = new Map();
    data.set("email", sessionStorage.getItem("email-rec"));

    let response = await fetch(restoreNewCodeUrl, {
        method: "PATCH",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "Request-Id": sessionStorage.getItem("request_id"),
        },
        body: JSON.stringify(Object.fromEntries(data)),
    });

    if (response.status === 200) {
        document
            .getElementById("get-code-wrapper-rec")
            .classList.add("display-off");
        document.getElementById("new-code-rec").classList.remove("display-off");
        document.getElementById("input-code-rec").value = "";

        if (isTimerGoingRec) {
            disableTimerRec(timerIdRec);
        }

        timerIdRec = showTimeRec(cooldownRec);
        isTimerGoingRec = true;
    }

    if (response.status === 404 || response.status === 425) {
        let error = await response.json();
        document.getElementById("new-pass-info").innerText =
            error["error"]["message"];
    }
}

document.getElementById("submit-rec").addEventListener("click", async (e) => {
    e.preventDefault();

    let password = document.getElementById("email-rec1").value;

    if (password != document.getElementById("email-rec2").value) {
        document.getElementById("new-pass-info").innerText =
            "passwords aren't match";
        return;
    }

    if (password.length < 6 || password.length > 20) {
        document.getElementById("new-pass-info").innerText =
            "username length must be between 6 and 20";
        return;
    }

    let response = await fetch(restoreVerifyUrl, {
        method: "Post",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "Request-Id": sessionStorage.getItem("request_id"),
            Device: getDeviceData(),
        },
        body: JSON.stringify({
            password: password,
            code: document.getElementById("input-code-rec").value,
        }),
    });

    if (response.status === 200) {
        closePasswordWindow();
        loadProfile();
    }
    if (response.status === 429 || response.status === 400) {
        error = await response.json();
        document.getElementById("new-pass-info").innerText =
            error["error"]["message"];
    }
});

function openPasswordWindow(email) {
    document.getElementById("email-rec").innerText = email;
    let window = document.getElementById("confirm-window-rec");
    window.style.opacity = 1;
    window.style.transform = "translate(0%)";
    window.style.visibility = "visible";

    document.getElementById("main-wrap").style.filter = "brightness(0.5)";
    document.getElementById("navbar").style.filter = "brightness(0.5)";
    disableButtons();
}

function closePasswordWindow() {
    if (isTimerGoingRec) {
        disableTimerRec(timerIdRec);
    }

    let window = document.getElementById("confirm-window-rec");
    window.style.opacity = 0;
    window.style.transform = "translate(200%)";
    document.getElementById("main-wrap").style.filter = "brightness(1)";
    document.getElementById("navbar").style.filter = "brightness(1)";
    document.getElementById("input-code-rec").value = "";
    document.getElementById("email-rec1").value = "";
    document.getElementById("email-rec2").value = "";
    document.getElementById("new-pass-info").innerText = "";

    setTimeout(() => {
        window.style.visibility = "hidden";
    }, 400);
    enableButtons();
}

let timerIdRec;
let isTimerGoingRec = false;

function showTimeRec(duration) {
    isTimerGoingRec = true;
    let minutes = Math.floor(duration / 60);
    let seconds = duration % 60;
    timerIdRec = setInterval(() => {
        let time;
        if (seconds < 10) {
            time = `${minutes}:0${seconds}`;
        } else {
            time = `${minutes}:${seconds}`;
        }
        document.getElementById("code-time-rec").innerHTML = time;
        if (seconds != 0) {
            seconds -= 1;
        } else {
            minutes -= 1;
            seconds = 59;
        }
    }, 1000);

    let thisTimerIdRec = timerIdRec;
    setTimeout(() => {
        if (thisTimerIdRec == timerIdRec && isTimerGoingRec) {
            disableTimerRec(timerIdRec);
            document
                .getElementById("new-code-rec")
                .classList.add("display-off");
            document
                .getElementById("get-code-wrapper-rec")
                .classList.remove("display-off");
        }
    }, (duration + 1) * 1000);

    return timerIdRec;
}

function disableTimerRec(timerID) {
    clearInterval(timerID);
    isTimerGoingRec = false;
}

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

// for (let i = 0; i < 10; i++) {

//     document.getElementsByClassName("term-btn")[i].addEventListener("click", () => {
//         let btn = this.classList()
//     })
// }
