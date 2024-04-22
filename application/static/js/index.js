document.getElementById("left-switch").onclick = leftSwitchTransform;

document.getElementById("right-switch").onclick = rightSwitchTransform;

document.getElementById("sign-up").onclick = openSignUpWindow;

document.getElementById("sign-in").onclick = openSignInWindow;

document.getElementById("sign-in-try").onclick = openSignInWindow;

document.getElementById("dropdown-sign-in").onclick = openSignInWindow;

document.getElementById("dropdown-sign-up").onclick = openSignUpWindow;

document.getElementById("cancel").onclick = closeLoginWindow;

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
}

function closeLoginWindow() {
  let loginWindow = document.getElementById("login");
  loginWindow.style.opacity = 0;
  loginWindow.style.transform = "translate(-100%, 30%)";
  document.getElementById("main").style.filter = "brightness(1)";
  document.getElementById("navbar").style.filter = "brightness(1)";
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