async function fetchJSON(url, options = {}) {
    const res = await fetch(url, options);
    const data = await res.json();
    if (data.status !== "success") {
        throw new Error(data.message);
    }
    return data;
}

async function sendOtp(email) {
    try {
        const res = await fetch("/auth/genOtp", {
            method: "POST",
            headers: { "content-Type": "application/json" },
            body: JSON.stringify({ "email": email })
        }
        );
        const data = await res.json();
        if (data.status == 'success') {
            Toastify({
                text: `OTP for ${email} Send Successfully.`,
                duration: 3000
            }).showToast();
            return data;
        }
        else {
            Toastify({
                text: data.message,
                duration: 3000
            }).showToast();
        }
    }
    catch (err) {
        Toastify({
            text: err.message,
            duration: 3000
        }).showToast();
    }
}

async function verifyOtp(email, otp, newPass, confirmPass) {
    try {
        const res = await fetch("/auth/otpVerification", {
            method: "POST",
            headers: { "content-Type": "application/json" },
            body: JSON.stringify({ "email": email, "otp": otp })
        })
        const data = await res.json();
        if (data.status !== 'success') {
            Toastify({
                text: data.message,
                duration: 3000
            }).showToast();
        }
        else {
            try {
                const result = await fetch("/user/resetPassword", {
                    method: "POST",
                    headers: { "content-Type": "application/json" },
                    body: JSON.stringify({ "email": email, "newPassword": newPass, "confirmPassword": confirmPass })
                })
                const dataReset = await result.json();
                if (dataReset.status == 'success') {
                    
                    Toastify({
                        text: dataReset.message,
                        duration: 3000
                    }).showToast();
                    window.location.href = "/login";
                }
                else {
                    Toastify({
                        text: dataReset.message,
                        duration: 3000
                    }).showToast();
                }
            }
            catch { }
        }
    }
    catch (err) {
        Toastify({
            text: err.message,
            duration: 3000
        }).showToast();
    }
}

$(document).on("submit", ".otpWrap", async function (e) {
    e.preventDefault();
    const data = new FormData(this)
    const result=sendOtp(data.get('email'))
    email=data.get('email')
    if (result.status === "success") {
        document.getElementById("regEmail").value = email;
    }
})

$(document).on("submit", "#resetPassword", async function (e) {
    e.preventDefault();
    const data = new FormData(this)
    const otp = data.get('otp')
    const newPass = data.get("newPassword")
    const confirmPass = data.get("confirmPassword")
    verifyOtp(email, otp, newPass, confirmPass)
})