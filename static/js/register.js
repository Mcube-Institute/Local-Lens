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

async function genOtp(email) {
    try {
        const response = await fetch("/tempEmailOtp/genOtp", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email
            })
        });

        const data = await response.json();

        if (data.status === "success") {
            Toastify({
                text: data.message,
                duration: 3000
            }).showToast();

            return data;
        } else {
            throw new Error(data.message);
        }

    } catch (err) {
        Toastify({
            text: err.message,
            duration: 3000
        }).showToast();
        throw err;
    }
}

async function verifyOtp(email, otp) {
    try {
        const res = await fetch("/tempEmailOtp/otpVerification",
            {
                method: "POST",
                headers: {
                    "content-type": "application/json"
                },
                body: JSON.stringify({
                    "email": email,
                    "otp": otp
                })
            }
        )

        const data = await res.json()
        if (data.status == 'success') {
            Toastify({
                text: data.message,
                duration: 3000
            }).showToast();
            return data;
        }
        else {
            throw new Error(data.message);

        }
    }
    catch (err) {
        Toastify({
            text: err.message,
            duration: 3000
        }).showToast();
        throw err;
    }
}

document.getElementById("otpGen").addEventListener("submit", async function (e) {
    e.preventDefault();

    const data = new FormData(this)
    const form = Object.fromEntries(data)

    email = form['email']
    const result = await genOtp(email)
    if (result.status === "success") {
        document.getElementById("regEmail").value = email;
        let seconds = 60;
        const timer = setInterval(() => {
            let btn = document.getElementById('submit')
            btn.innerText = seconds;
            btn.disabled = true;
            seconds--;
            if (seconds < 0) {
                clearInterval(timer)
                btn.innerText = 'OTP';
                btn.disabled = false;
            }
        }, 1000)
    }

})

document.getElementById("registerForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const form = new FormData(this)
    const data = Object.fromEntries(form)

    otp = data['otp']

    try {
        const verOtp = await verifyOtp(email, otp);

        if (verOtp.status === "success") {
            register(data);
        }
    } catch (err) {
        throw new Error(err);

    }
})