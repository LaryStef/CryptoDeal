var url = new URL("api/auth/sign-up", location.origin);

document.getElementById("login-form-id").addEventListener("submit", async (e) => {
    e.preventDefault();

    let formData = new FormData(document.getElementById("login-form-id"));

    let response = await fetch(url, {
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
