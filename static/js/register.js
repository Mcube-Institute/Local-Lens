function register(data) {
    fetch("/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.status == "success") {
                window.location.replace("/");
                alert(data.message)
            }
            else {
                throw new Error(data.message);
            }
        })
        .catch(err => {
            alert(err)
        })
}

document.getElementById("registerForm").addEventListener("submit",function(e){
    e.preventDefault();
    
    const form=new FormData(this)
    const data=Object.fromEntries(form)

    register(data)
})