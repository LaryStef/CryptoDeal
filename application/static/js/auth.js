var loginUrl = new URL("api/auth/sign-in", location.origin);
var registerUrl = new URL("api/auth/sign-up", location.origin);


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
        console.log(result);
    } else {
        console.log(response.status);
    }
})

document.getElementById("register-form-id").addEventListener("submit", async (e) => {
    e.preventDefault();

    let formData = new FormData(document.getElementById("register-form-id"));

    let response = await fetch(registerUrl, {
        method: "POST",
        credentials: "same-origin",
        body: formData
    });
    
    if (response.status == 200) {
        let result = await response.json();
        console.log(result);
    } else {
        console.log(response.status);
    }
})