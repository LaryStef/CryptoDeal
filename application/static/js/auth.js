document.getElementById("left-switch").onclick = leftSwitchTransform;

document.getElementById("right-switch").onclick = rightSwitchTransform;

document.getElementById("sign-up").onclick = openSignUpWindow;

document.getElementById("sign-in").onclick = openSignInWindow;

document.getElementById("sign-in-try").onclick = openSignInWindow;

document.getElementById("dropdown-sign-in").onclick = openSignInWindow;

document.getElementById("dropdown-sign-up").onclick = openSignUpWindow;

document.getElementById("cancel").onclick = closeLoginWindow;

document.getElementById("mail-cancel").onclick = closeConfirmWindow;

document.getElementById("code-btn").onclick = sendNewCode;

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
  document.getElementById("register-container").classList.add("transition-off");
  document.getElementById("login-container").classList.add("transition-off");

  leftSwitchTransform();
  setTimeout(() => {
    document.getElementById("mode-light").classList.remove("transition-off");
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

function openConfirmWindow() {
  document.getElementById("email").innerHTML = document.getElementById("email-input").value;
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
  document.getElementById("login-info").innerText = "";
  document.getElementById("register-info").innerText = "";
  setTimeout(() => {
    window.style.visibility = "hidden";
  }, 400)
  enableButtons();
  if (isTimerGoing) {
    disableTimer(timerId);
  }
}

document.addEventListener("input", () => {
  let field = document.getElementById("input-code")
  if (field.value.length === 6) {
    field.style.backgroundColor = "#BF1A3E";

    // send check code request
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


var loginUrl = new URL("api/auth/sign-in", location.origin);
var registerUrl = new URL("api/auth/sign-up", location.origin);
var newCodeUrl = new URL("api/auth/refresh-code", location.origin);

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


  document.getElementById("get-code-wrapper").classList.add("display-off");
  document.getElementById("new-code").classList.remove("display-off");
  document.getElementById("input-code").style.backgroundColor = "#7d42e7";
  document.getElementById("input-code").value = "";
  timerId = showTime(15);
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
      let result = await response.json();
      document.getElementById("login-info").innerHTML = "successful " + response.status;
  } else {
      console.log(response.status);
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
      timerId = showTime(15);
  
      closeLoginWindow();
      openConfirmWindow();
    }
    else {
      error = await response.text();
      document.getElementById("register-info").innerHTML = error.substring(1, error.length - 2);
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