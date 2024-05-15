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
  let window = document.getElementById("confirm-window");
  window.style.opacity = 1;
  window.style.transform = "translate(0%)";
  window.style.visibility = "visible";
  document.getElementById("main").style.filter = "brightness(0.5)";
  document.getElementById("navbar").style.filter = "brightness(0.5)";
  disableButtons();
  if (!showTimeStarted) {
    showTime(20);
  }
}

function closeConfirmWindow() {
  let window = document.getElementById("confirm-window");
  window.style.opacity = 0;
  window.style.transform = "translate(200%)";
  document.getElementById("main").style.filter = "brightness(1)";
  document.getElementById("navbar").style.filter = "brightness(1)";
  setTimeout(() => {
    window.style.visibility = "hidden";
  }, 400)
  enableButtons();
}

document.addEventListener("input", () => {
  let field = document.getElementById("input-code")
  if (field.value.length === 6) {
    field.style.backgroundColor = "#BF1A3E";
  }
})

var showTimeStarted = false;

function showTime(duration) {
  showTimeStarted = true;
  let minutes = Math.floor(duration / 60);
  let seconds = duration % 60;
  let timerId = setInterval(() => {
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
  
  setTimeout(() => {
    clearInterval(timerId);
    showSendMailButton();
  }, (duration + 1) * 1000);
}

// function clearInt(timerId) {
//   clearInterval(timerId);
//   showSendMailButton();
// }

function showSendMailButton() {
  document.getElementById("new-code").classList.add("display-off");
  document.getElementById("get-code-wrapper").classList.remove("display-off");
}

function sendNewCode() {
  // send new code request to server

  document.getElementById("get-code-wrapper").classList.add("display-off");
  document.getElementById("new-code").classList.remove("display-off");
  document.getElementById("input-code").style.backgroundColor = "#7d42e7";
  document.getElementById("input-code").value = "";
  showTime(20);
}


var loginUrl = new URL("api/auth/sign-in", location.origin);
var registerUrl = new URL("api/auth/sign-up", location.origin);

document.getElementById("login-form-id").addEventListener("submit", async (e) => {
    e.preventDefault();

    let formData = new FormData(document.getElementById("login-form-id"));
    formData.append("page", window.location.href);
    
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
  formData.append("page", window.location.href);
  
  // let response = await fetch(registerUrl, {
    //     method: "POST",
    //     credentials: "same-origin",
    //     body: formData
    // });
    
    closeLoginWindow();
    openConfirmWindow();
    
    // if (response.status == 200) {
      //     localStorage.set("request_id", response.headers.get("Request-Id"));
      //     closeLoginWindow();
      //     openConfirmWindow();
    // } else {
    //     document.getElementById("login-info").innerHTML = "successful";
    // }
  })
  
//openConfirmWindow();