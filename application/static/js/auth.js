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

    let response = await fetch(registerUrl, {
        method: "POST",
        credentials: "same-origin",
        body: formData
    });
    
    if (response.status == 200) {
        localStorage.set("request_id", response.headers.get("Request-Id"));
        
    } else {
        document.getElementById("login-info").innerHTML = "successful";
    }
})

