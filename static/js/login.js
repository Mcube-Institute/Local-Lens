function logIn(data) {
    console.log(data)
    fetch("/auth/logIn", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.status == "success") {
                $(".logOut").removeClass("visually-hidden");
                $(".logIn").addClass("visually-hidden");
                window.location.replace("/");
                 Toastify({
                text: data.message,
                duration: 3000
            }).showToast();
            }
            else {
                throw new Error(data.message);
            }
        })
        .catch(err => {
             Toastify({
                text: err.message,
                duration: 3000
            }).showToast();
        })
}

document.getElementById("loginForm").addEventListener("submit",function(e){
        e.preventDefault();
    
    const form=new FormData(this)
    const data=Object.fromEntries(form)

    logIn(data)
})