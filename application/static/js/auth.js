const loginUrl = new URL("api/auth/sign-in", location.origin);
const registerUrl = new URL("api/auth/sign-up", location.origin);
const newCodeUrl = new URL("api/auth/refresh-code", location.origin);
const restoreUrl = new URL("api/auth/restore", location.origin);
const verifyCodeUrl = new URL("api/auth/verify-code", location.origin);

const cooldown = 30;
const cooldownRec = 30;


document.getElementById("left-switch").onclick = leftSwitchTransform;
document.getElementById("right-switch").onclick = rightSwitchTransform;
document.getElementById("sign-up").onclick = openSignUpWindow;
document.getElementById("sign-in").onclick = openSignInWindow;
document.getElementById("sign-in-try").onclick = openSignUpWindow;

document.getElementById("dropdown-sign-in").onclick = openSignInWindow;
document.getElementById("dropdown-sign-up").onclick = openSignUpWindow;

document.getElementById("cancel").onclick = closeLoginWindow;
document.getElementById("mail-cancel").onclick = closeConfirmWindow;
document.getElementById("email-cancel").onclick = closeEmailWindow;
document.getElementById("mail-cancel-rec").onclick = closePasswordWindow;

document.getElementById("code-btn").onclick = sendNewCode;
document.getElementById("code-btn-rec").onclick = sendNewCodeRec;


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
  document.getElementById("register-container").classList.add("transition-off");
  document.getElementById("login-container").classList.add("transition-off");

  rightSwitchTransform();
  setTimeout(() => {
    document.getElementById("mode-light").classList.remove("transition-off");
    document.getElementById("register-container").classList.remove("transition-off");
    document.getElementById("login-container").classList.remove("transition-off");
  }, 400);
}

function leftSwitch() {
  document.getElementById("mode-light").classList.add("transition-off");
  document.getElementById("register-container").classList.add("transition-off");
  document.getElementById("login-container").classList.add("transition-off");

  leftSwitchTransform();
  setTimeout(() => {
    document.getElementById("mode-light").classList.remove("transition-off");
    document.getElementById("register-container").classList.remove("transition-off");
    document.getElementById("login-container").classList.remove("transition-off");
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
  document.getElementById("main").style.filter = "brightness(0.5)";
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
  document.getElementById("main").style.filter = "brightness(0.5)";
  document.getElementById("navbar").style.filter = "brightness(0.5)";
  disableButtons();
}

function closeLoginWindow() {
  let loginWindow = document.getElementById("login");
  loginWindow.style.opacity = 0;
  loginWindow.style.transform = "translate(-100%, 30%)";
  document.getElementById("main").style.filter = "brightness(1)";
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

  document.getElementById("main").style.filter = "brightness(0.5)";
  document.getElementById("navbar").style.filter = "brightness(0.5)";
  disableButtons();
}

function closeConfirmWindow() {
  let window = document.getElementById("confirm-window");
  window.style.opacity = 0;
  window.style.transform = "translate(200%)";
  document.getElementById("main").style.filter = "brightness(1)";
  document.getElementById("navbar").style.filter = "brightness(1)";
  document.getElementById("input-code").style.backgroundColor = "#7d42e7";
  document.getElementById("input-code").value = "";

  setTimeout(() => {
    window.style.visibility = "hidden";
  }, 400)
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
})


var timerId;
var isTimerGoing = false;

function showTime(duration) {
  isTimerGoing = true;
  let minutes = Math.floor(duration / 60);
  let seconds = duration % 60;
  timerId = setInterval(() => {
    var time;
    if (seconds < 10) {
      time = `${minutes}:0${seconds}`;
    }
    else {
      time = `${minutes}:${seconds}`;
    }
    document.getElementById("code-time").innerHTML = time;
    if (seconds != 0) {
      seconds -= 1;
    }
    else {
      minutes -= 1;
      seconds = 59;
    }
  }, 1000);
  
  let thisTimerId = timerId;
  setTimeout(() => {
    if (thisTimerId == timerId) {
      disableTimer(timerId);
      document.getElementById("new-code").classList.add("display-off");
      document.getElementById("get-code-wrapper").classList.remove("display-off");
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
      "Request-Id": sessionStorage.getItem("request_id")
    },
    body: JSON.stringify(Object.fromEntries(data))
  });

  if (response.status == 200) {
    closeConfirmWindow();

    // show profile
  } else {
    document.getElementById("input-code").style.backgroundColor = "#BF1A3E";
  }
}

async function sendNewCode() {
  let data = new Map();
  data.set("email", document.getElementById("email-input").value);

  response = await fetch(newCodeUrl, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "Request-Id": sessionStorage.getItem("request_id")
    },
    body: JSON.stringify(Object.fromEntries(data))
  });

  if (response.status == 200) {
    document.getElementById("get-code-wrapper").classList.add("display-off");
    document.getElementById("new-code").classList.remove("display-off");
    document.getElementById("input-code").style.backgroundColor = "#7d42e7";
    document.getElementById("input-code").value = "";
    timerId = showTime(cooldown);
  }
}

document.getElementById("login-form-id").addEventListener("submit", async (e) => {
  e.preventDefault();

  let formData = new FormData(document.getElementById("login-form-id"));
  
  let response = await fetch(loginUrl, {
    method: "POST",
    credentials: "same-origin",
    body: formData
  });
  
  if (response.status == 200) {
    closeLoginWindow();
  } else {
      let error = await response.json();
      document.getElementById("login-info").innerHTML = error["error"]["message"];
  }
})

document.getElementById("register-form-id").addEventListener("submit", async (e) => {
  e.preventDefault();

  let formData = new FormData(document.getElementById("register-form-id"));

  if (validateRegisterData(formData)) {
    let response = await fetch(registerUrl, {
      method: "POST",
      credentials: "same-origin",
      body: formData
    });
  
    if (response.status == 201) {
      if (isTimerGoing) {
        disableTimer(timerId);
      }
  
      sessionStorage.setItem("request_id", response.headers.get("Request-Id"));
      
      document.getElementById("get-code-wrapper").classList.add("display-off");
      document.getElementById("new-code").classList.remove("display-off");
      document.getElementById("input-code").style.backgroundColor = "#7d42e7";
      document.getElementById("input-code").value = "";
      timerId = showTime(cooldown);
  
      closeLoginWindow();
      openConfirmWindow(document.getElementById("email-input").value);
    }
    else {
      error = await response.json();
      document.getElementById("register-info").innerHTML = error["error"]["message"];
    }
  }
})

function validateRegisterData(formData) {
  const re = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
  
  let username = formData.get("username");
  let pass = formData.get("password");
  let email = formData.get("email");

  if (username.length < 6 || username.length > 20) {
    document.getElementById("register-info").innerText = "username length must be between 6 and 20";
    return false;
  }
  if (username.includes(" ")) {
    document.getElementById("register-info").innerText = "username can't include any spaces";
    return false;
  }
  if (pass.length < 6 || pass.length > 20) {
    document.getElementById("register-info").innerText = "password length must be between 6 and 20";
    return false;
  }
  if (pass.includes(" ")) {
    document.getElementById("register-info").innerText = "password can't include any spaces";
    return false;
  }
  if (!re.test(email)) {
    document.getElementById("register-info").innerText = "invalid email";
    return false;
  }

  return true;
}

function openEmailWindow() {
  let window = document.getElementById("email-window");
  window.style.opacity = 1;
  window.style.transform = "translate(0%)";
  window.style.visibility = "visible";

  document.getElementById("main").style.filter = "brightness(0.5)";
  document.getElementById("navbar").style.filter = "brightness(0.5)";
  disableButtons();
}

function closeEmailWindow() {
  let window = document.getElementById("email-window");
  window.style.opacity = 0;
  window.style.transform = "translate(-200%)";
  document.getElementById("main").style.filter = "brightness(1)";
  document.getElementById("navbar").style.filter = "brightness(1)";
  document.getElementById("email-input-recovery").value = "";
  
  setTimeout(() => {
    window.style.visibility = "hidden";
    window.style.transition = "none";
    window.style.transform = "translate(200%)";
    window.style.transition = "all var(--login-transition-duration) ease-out";
  }, 400)
  
  enableButtons();
}

function openPasswordWindow(email) {
  document.getElementById("email-rec").innerText = email;
  let window = document.getElementById("confirm-window-rec");
  window.style.opacity = 1;
  window.style.transform = "translate(0%)";
  window.style.visibility = "visible";

  document.getElementById("main").style.filter = "brightness(0.5)";
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
  document.getElementById("main").style.filter = "brightness(1)";
  document.getElementById("navbar").style.filter = "brightness(1)";
  document.getElementById("input-code-rec").style.backgroundColor = "#7d42e7";
  document.getElementById("input-code-rec").value = "";
  document.getElementById("email-rec1").value = "";
  document.getElementById("email-rec2").value = "";

  setTimeout(() => {
    window.style.visibility = "hidden";
  }, 400)
  enableButtons();
}

document.getElementById("recovery-btn").addEventListener("click", () => {
  closeLoginWindow();
  openEmailWindow();
})


var timerIdRec;
var isTimerGoingRec = false;

function showTimeRec(duration) {
  isTimerGoingRec = true;
  let minutes = Math.floor(duration / 60);
  let seconds = duration % 60;
  timerIdRec = setInterval(() => {
    var time;
    if (seconds < 10) {
      time = `${minutes}:0${seconds}`;
    }
    else {
      time = `${minutes}:${seconds}`;
    }
    document.getElementById("code-time-rec").innerHTML = time;
    if (seconds != 0) {
      seconds -= 1;
    }
    else {
      minutes -= 1;
      seconds = 59;
    }
  }, 1000);
  
  let thisTimerIdRec = timerIdRec;
  setTimeout(() => {
    if (thisTimerIdRec == timerIdRec && isTimerGoingRec) {
      disableTimerRec(timerIdRec);
      document.getElementById("new-code-rec").classList.add("display-off");
      document.getElementById("get-code-wrapper-rec").classList.remove("display-off");
    }
  }, (duration + 1) * 1000);

  return timerIdRec;
}

async function sendNewCodeRec() {
  // let data = new Map();
  // data.set("email", document.getElementById("email-input").value);

  // let response = await fetch(newCodeUrl, {
  //   method: "POST",
  //   credentials: "same-origin",
  //   headers: {
  //     "Content-Type": "application/json",
  //     "Request-Id": sessionStorage.getItem("request_id")
  //   },
  //   body: JSON.stringify(Object.fromEntries(data))
  // });

  // if (response.status == 200) {
  //   document.getElementById("get-code-wrapper").classList.add("display-off");
  //   document.getElementById("new-code").classList.remove("display-off");
  //   document.getElementById("input-code").style.backgroundColor = "#7d42e7";
  //   document.getElementById("input-code").value = "";
  //   timerId = showTime(cooldown);
  // }
  document.getElementById("get-code-wrapper-rec").classList.add("display-off");
  document.getElementById("new-code-rec").classList.remove("display-off");
  document.getElementById("input-code-rec").value = "";

  if (isTimerGoingRec) {
    disableTimerRec(timerIdRec);
  }

  timerIdRec = showTimeRec(cooldownRec);
  isTimerGoingRec = true
}

document.getElementById("email-submit").addEventListener("click", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email-input-recovery").value;

  let data = new Map();
  data.set("email", email);

  let response = await fetch(restoreUrl, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(Object.fromEntries(data))
  })

  if (response.status === 201) {
    closeEmailWindow();
    openPasswordWindow(email);
    if (isTimerGoingRec) {
      disableTimerRec(timerIdRec);
    }

    document.getElementById("get-code-wrapper-rec").classList.add("display-off");
    document.getElementById("new-code-rec").classList.remove("display-off");
    timerIdRec = showTimeRec(cooldownRec);

    sessionStorage.setItem("request_id", response.headers.get("Request-Id"));
  } else if (response.status === 404 || response.status === 425) {
    let error = await response.json();
    document.getElementById("pass-info").innerText = error["error"]["message"];
  }
})

document.getElementById("submit-rec").addEventListener("click", (e) => {
  e.preventDefault();

})

function disableTimerRec(timerID) {
  clearInterval(timerID);
  isTimerGoingRec = false;
}