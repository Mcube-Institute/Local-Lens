/* Utility  */

document.addEventListener("DOMContentLoaded", () => {
    const reveals = document.querySelectorAll(".reveal");

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("active");
                    observer.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.05   // 👈 instead of 0.15
        }
    );

    reveals.forEach(el => observer.observe(el));
});

function getDateTime(dateTime) {
    const d = new Date(dateTime);

    const day = d.getDate();
    const month = d.toLocaleString("en-IN", { month: "short",timeZone: "Asia/Kolkata" }); // Jan, Feb, Mar
    const year = d.getFullYear();

    return `${day} ${month} ${year}`;
}


document.querySelectorAll(".myIssue, .localIssue").forEach(section => {
    section.addEventListener("scroll", () => {
        section.classList.toggle("scrolled", section.scrollTop > 10);
    });
});

/*------ Utility ------*/

/* Dynamic Issue Loading */

function issueCard(issue) {
    const stColorMap = {
        "REPORTED": "statusReported",
        "IN_PROGRESS": "statusProgress",
        "RESOLVED": "statusResolved",
        "CLOSED": "statusClosed"
    };

    return `

    <div class="issue">
                    <div class="issueTop p-2 pe-0">
                        <h4 class="issueTittle reveal ">${issue.issueTittle}</h4>
                        <h5 class="status ${stColorMap[issue.status]} reveal">${issue.status.replace("_", " ")}</h5>
                    </div>
                    <div class="issueBottom p-2 px-0 pe-1 pb-0">
                        <p class="reveal p-3 px-2">Category : <span class="category">${issue.category}</span></p>
                        <a role="button"
                            class="link-info link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover reveal view"
                            data-bs-toggle="modal" data-bs-target="#viewIssueModal" data-id=${issue.id}>
                            VIEW
                        </a>
                    </div>
                </div>

    `;
}

function trackUpdate(issues, filter = "all") {
    let total = 0;
    let inProgress = 0;
    let resolved = 0;
    let closed = 0;

    const now = new Date();

    issues.forEach(issue => {
        const createdAt = new Date(issue.createdAt);
        let include = true;

        switch (filter) {
            case "24h":
                include = createdAt >= new Date(now.getTime() - 24 * 60 * 60 * 1000);
                break;

            case "7d":
                include = createdAt >= new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
                break;

            case "1m":
                include = createdAt >= new Date(
                    now.getFullYear(),
                    now.getMonth() - 1,
                    now.getDate()
                );
                break;

            case "1y":
                include = createdAt >= new Date(
                    now.getFullYear() - 1,
                    now.getMonth(),
                    now.getDate()
                );
                break;

            case "all":
            default:
                include = true;
        }

        if (!include) return;

        total++;

        if (issue.status === "IN_PROGRESS") inProgress++;
        if (issue.status === "RESOLVED") resolved++;
        if (issue.status === "CLOSED") closed++;
    });

    $(".totalCount").text(total);
    $(".inprogressCount").text(inProgress);
    $(".resolvedCount").text(resolved);
    $(".closedCount").text(closed);
}

function getIssues() {
    fetch("/issue/getAll")
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                allIssues = data.data;

                const localIssue = $("#localIssueContainer");
                localIssue.empty();

                allIssues.forEach(issue => {
                    localIssue.append(issueCard(issue));
                });

                trackUpdate(allIssues, "all");
                $(".reveal").addClass("active");
            }
        })
        .catch(err => alert(err.message));
}

$(document).on("click", "#trackFilter button", function () {
    $("#trackFilter button").removeClass("active");
    $(this).addClass("active");

    const filter = $(this).data("filter");
    trackUpdate(allIssues, filter);
});


function getUserIssues() {
    fetch("/issue/getAll?isUser=true")
        .then(res => res.json())
        .then(data => {
            if (data.status == "success") {
                const issues = data.data;
                const myIssue = $("#myIssueContainer");
                myIssue.empty();
                if(!data.isLogIn){
                    myIssue.html(`
                       <div class="emptyIssue reveal">
                    <i class="bi bi-inbox-fill reveal"></i>
                    <p class="reveal">No Issues Reported Yet.</p>
                    <a class="logIn btn btn-primary px-4  py-2"  href="/login"><i class="bi bi-box-arrow-in-right pe-2"></i>logIn</a></li>
                    `);
                }

                if (data.isLogIn) {
                    console.log("In")
                    issues.forEach(issue => {
                        myIssue.append(issueCard(issue));
                    })
                }

                console.log("out")

                if (myIssue.children().length === 0) {
                    myIssue.html(`
                       <div class="emptyIssue reveal">
                    <i class="bi bi-inbox-fill reveal"></i>
                    <p class="reveal">No Issues Reported Yet.</p>
                    <button type="button" class="btn btn-primary reportNew px-4  py-2 reveal" data-bs-toggle="modal"
                        data-bs-target="#reportIssueModal"><i class="bi bi-plus-circle-dotted"></i> Report New
                        Issue</button>
                        </div>
                    `);
                }
                if (data.isLogIn) {
                    trackUpdate(issues);
                }
                $(".reveal").addClass("active")
            }

            else {
                throw new Error(data.message);
            }
        })
        .catch(err => alert(err.message))
}

$(document).ready(function () {
    getIssues();
    getUserIssues();
});

async function getLocation(location) {
    try {
        const res = await fetch(`/location/getSpecific?id=${location}`);
        const data = await res.json();

        if (data.status === "success") {
            return data.data;
        } else {
            throw new Error(data.message);
        }
    } catch (err) {
        alert(err.message);
        return null;
    }
}


$(document).on("click", ".view", async function () {

    const stColorMap = {
        "REPORTED": "statusReported",
        "IN_PROGRESS": "statusProgress",
        "RESOLVED": "statusResolved",
        "CLOSED": "statusClosed"
    };

    const issueId = $(this).data("id");

    try {
        const res = await fetch(`/issue/getSpecific?id=${issueId}`);
        const data = await res.json();
        

        if (data.status !== "success") {
            throw new Error(data.message);
        }

        const issue = data.data;
        const attachments = issue.imagePath;
        const modal = $("#viewIssueModal");

        modal.find(".status")
            .removeClass("statusProgress statusReported statusResolved statusClosed")
            .addClass(stColorMap[issue.status])
            .text(issue.status.replace("_", " "));

        const assignedTo=issue.assignedTo;

        const result=await fetch(`/user/getSpecific?id=${assignedTo}`)
        const userJson=await result.json();

        if (userJson.status !== "success") {
            throw new Error(data.message);
        }
        user=userJson.data;

        modal.find(".reportedOn").text(getDateTime(issue.createdAt));
        modal.find(".issueTittle").text(issue.issueTittle);
        modal.find(".issueDescription").text(issue.issueDescription);
        modal.find(".issueCategory").text(issue.category);
        modal.find(".assignedToName").text(user.name);
        modal.find(".assignedToEmail").text(user.email);

        const issueLocation = await getLocation(issue.location);

        if (issueLocation) {
            modal.find(".street").text(issueLocation.street);
            modal.find(".city").text(issueLocation.city);
            modal.find(".state").text(issueLocation.state);
            modal.find(".country").text(issueLocation.country);
            modal.find(".pincode").text(issueLocation.pincode);
        }

        const imageGroup = $(".imageGroup");
        imageGroup.empty();

        attachments.forEach(file => {

            const ext = file.split(".").pop().toLowerCase();

            const imageExts = ["jpg", "jpeg", "png", "gif", "webp", "dng"];
            const videoExts = ["mp4", "webm", "ogg"];

            if (imageExts.includes(ext)) {
                imageGroup.append(`
            <img src="${file}" alt="attachment" class="attachments">
        `);
            }
            else if (videoExts.includes(ext)) {
                imageGroup.append(`
            <video class="attachments" controls>
                <source src="${file}" type="video/${ext}">
                Your browser does not support the video tag.
            </video>
        `);
            }
        });

    } catch (err) {
        alert(err.message);
    }
});

/*  Issue Creation   */

function createLocation(locationData) {
    return fetch("/location/new", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(locationData)
    }).then(res => res.json());
}

function createIssue(data) {
    console.log(data)
    fetch("/issue/new", {
        method: "POST",
        body: data
    })
        .then(response => response.json())
        .then(data => {
            if (data.status == "success") {
                $("#reportIssueModal").modal("hide");
                getIssues();
                getUserIssues();
                refreshNotificationDot();
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

$(".issueCreation").on("submit", function (e) {
    e.preventDefault();

    const data = new FormData(document.getElementById("issueForm"));
    // const data = Object.fromEntries(formData);
    console.log("Up....")
    console.log(data)
    const locationData = {
        street: data.get("street"),
        city: data.get("city"),
        state: data.get("state"),
        country: data.get("country"),
        pincode: data.get("pincode")
    };

    console.log("Down....")
    console.log(locationData)
    createLocation(locationData)
        .then(locRes => {
            if (locRes.status !== "success") {
                throw new Error(locRes.message);
            }

            data.append("locationId", locRes.data.id)

            // const issueData = {
            //     issueTittle: data.issueTittle,
            //     issueDescription: data.issueDescription,
            //     category: data.category,
            //     tags: data.tags,
            //     locationId: locRes.data.id
            // };

            const files = document.getElementById("attachments").files;

            if (files.length === 0) {
                alert("Please select files");
                return;
            }

            /* if (files.length > 1) {
                for (let file of files) {
                    data.append("attachments", file);
                }
            } */

            console.log(data)
            createIssue(data)
        })
        .catch(err => {
            alert(err.message);
        });
});

/* Notification */

function getStatusFromMessage(message) {
    const msg = message.toLowerCase();

    if (msg.startsWith("issue reported")) {
        return { prev: null, next: "REPORTED" };
    }
    if (msg.includes("now in_progress")) {
        return { prev: "REPORTED", next: "IN_PROGRESS" };
    }
    if (msg.includes("been resolved")) {
        return { prev: "IN_PROGRESS", next: "RESOLVED" };
    }
    if (msg.includes("been closed")) {
        return { prev: "RESOLVED", next: "CLOSED" };
    }
    return null;
}


function notificationCard(n, issue) {

    const stColorMap = {
        REPORTED: "statusReported",
        IN_PROGRESS: "statusProgress",
        RESOLVED: "statusResolved",
        CLOSED: "statusClosed"
    };

    const flow = getStatusFromMessage(n.message);

    const statusHTML = !flow || !flow.prev
        ? `<span class="statusNew ${stColorMap.REPORTED}">REPORTED</span>`
        : `
            <span class="statusOld ${stColorMap[flow.prev]}">
                ${flow.prev.replace("_", " ")}
            </span>
            <i class="bi bi-arrow-right"></i>
            <span class="statusNew ${stColorMap[flow.next]}">
                ${flow.next.replace("_", " ")}
            </span>
          `;

    return `
        <div class="notificationItem ${!n.isViewed ? "unread" : ""}"
             data-id="${n.id}">

            <div class="notificationHeader">
                <div class="notificationTitle">
                    ${issue.issueTittle}
                </div>

                <div class="notificationStatus">
                    ${statusHTML}
                </div>
            </div>

            <div class="notificationTime">
                ${getDateTime(n.createdAt)}
            </div>

            <div class="notificationMessage">
                ${n.message}
            </div>
        </div>
    `;
}


async function refreshNotificationDot() {
    const res = await fetch("/notification/getAll");
    const data = await res.json();

    if (data.status !== "success") return;

    const hasUnread = data.data.some(n => !n.isViewed);

    if (hasUnread) {
        $("#notificationDot").show();
    } else {
        $("#notificationDot").hide();
    }
}


async function loadNotifications() {
    const res = await fetch("/notification/getAll");
    const data = await res.json();
    if (data.status !== "success") return;

    const allTab = $("#all");
    const reportedTab = $("#reported");
    const progressTab = $("#progress");
    const resolvedTab = $("#resolved");
    const closedTab = $("#closed");

    allTab.empty();
    reportedTab.empty();
    progressTab.empty();
    resolvedTab.empty();
    closedTab.empty();

    for (let n of data.data) {

        const issueRes = await fetch(`/issue/getSpecific?id=${n.issue}`);
        const issueData = await issueRes.json();
        if (issueData.status !== "success") continue;

        const issue = issueData.data;
        const card = notificationCard(n, issue);

        allTab.append(card);

        const msg = n.message.toLowerCase();

        if (msg.startsWith("issue reported")) {
            reportedTab.append(card);
        }
        else if (msg.includes("in_progress")) {
            progressTab.append(card);
        }
        else if (msg.includes("resolved")) {
            resolvedTab.append(card);
        }
        else if (msg.includes("closed")) {
            closedTab.append(card);
        }
    }
}


$(document).on("click", ".notificationItem", async function () {
    const id = $(this).data("id");

    if (!$(this).hasClass("unread")) return;

    await fetch(`/notification/view?id=${id}`, { method: "POST" });

    $(this).removeClass("unread");

    refreshNotificationDot();
});


$("#notificationModal").on("shown.bs.offcanvas", async function () {
    await loadNotifications();
});


$(document).ready(() => {
    refreshNotificationDot();
});
