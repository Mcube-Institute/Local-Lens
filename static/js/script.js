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
    const month = d.toLocaleString("en-IN", { month: "short" }); // Jan, Feb, Mar
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

function trackUpdate(issues) {
    let inProgress = 0;
    let resolved = 0;
    let closed = 0;

    issues.forEach(issue => {
        if (issue.status == "IN_PROGRESS") inProgress++;
        if (issue.status == "RESOLVED") resolved++;
        if (issue.status == "CLOSED") closed++;
    })

    $(".totalCount").text(issues.length);
    $(".inprogressCount").text(inProgress)
    $(".closedCount").text(closed)
    $(".resolvedCount").text(resolved)
}

function getIssues() {
    fetch("/issue/getAll")
        .then(res => res.json())
        .then(data => {
            if (data.status == "success") {
                const issues = data.data;
                const myIssue = $("#myIssueContainer");
                const localIssue = $("#localIssueContainer")

                myIssue.empty();
                localIssue.empty();

                const userId = $(".user").data("userid");

                issues.forEach(issue => {
                    if (issue.user.id == userId) {
                        myIssue.append(issueCard(issue));
                    }
                    else {
                        localIssue.append(issueCard(issue));
                    }
                })

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

                if (localIssue.children().length === 0) {
                    localIssue.html(`
                        <div class="emptyIssue reveal">
                            <i class="bi bi-geo-alt-fill"></i>
                            <p>No Issues Found In Your Locality.</p>
                        </div>
                    `);
                }

                trackUpdate(issues);
                $(".reveal").addClass("active")
            }

            else {
                throw new Error(data.message);
            }
        })
        .catch(err => alert(err.message))
}

$(document).ready(getIssues);

function getLocation(location) {
    fetch(`/location/getSpecific?id=${location}`)
        .then(res => res.json())
        .then(data => {
            if (data.status == "success") {
                const issueLocation = data.data;
                const modal = $("#viewIssueModal");
                modal.find(".street").text(issueLocation.street);
                modal.find(".city").text(issueLocation.city);
                modal.find(".state").text(issueLocation.state);
                modal.find(".country").text(issueLocation.country);
                modal.find(".pincode").text(issueLocation.pincode);
            }
            else {
                throw new Error(data.message);
            }
        })
        .catch(err => alert(err.message))
}

$(document).on("click", ".view", function () {

    const stColorMap = {
        "REPORTED": "statusReported",
        "IN_PROGRESS": "statusProgress",
        "RESOLVED": "statusReported",
        "CLOSED": "statusClosed"
    };

    const issueId = $(this).data("id");

    fetch(`/issue/getSpecific?id=${issueId}`)
        .then(res => res.json())
        .then(data => {
            if (data.status == "success") {
                const issue = data.data;
                attachments = issue.imagePath;

                const modal = $("#viewIssueModal");

                modal.find(".status")
                    .removeClass("statusProgress statusReported statusResolved statusClosed");
                modal.find(".status").addClass(stColorMap[issue.status]).text(issue.status.replace("_", " "));
                $("#viewIssueModal .reportedOn").text(getDateTime(issue.createdAt));
                $("#viewIssueModal .issueTittle").text(issue.issueTittle);
                $("#viewIssueModal .issueDescription").text(issue.issueDescription);
                $("#viewIssueModal .issueCategory").text(issue.category);
                getLocation(issue.location)

                imageGroup = $(".imageGroup");
                imageGroup.empty();
                console.log(attachments)

                for (let index = 0; index < attachments.length; index++) {
                    imageGroup.append(`<img src="${attachments[index]}" alt="attachments"
                                class="attachments">`)
                }

            }
            else {
                throw new Error(data.message);
            }
        })
        .catch(err => alert(err.message));
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

            if (files.length > 1) {
                for (let file of files) {
                    data.append("attachments", file);
                }
            }

            console.log(data)
            createIssue(data)
        })
        .catch(err => {
            alert(err.message);
        });
});

/* Notification */

function notificationCard() {

    const stColorMap = {
        "REPORTED": "statusReported",
        "IN_PROGRESS": "statusProgress",
        "RESOLVED": "statusResolved",
        "CLOSED": "statusClosed"
    };

    return `<div class="notificationItem unread reveal">
                        <div class="notificationHeader">
                            <div class="notificationTitle">
                                ${a}
                            </div>

                            <div class="notificationStatus">
                                <span class="statusOld statusReported px-1 text-nowrap">REPORTED</span>
                                <i class="bi bi-arrow-right"></i>
                                <span class="statusNew statusProgress px-1 text-nowrap">IN PROGRESS</span>
                            </div>
                        </div>

                        <div class="notificationTime">
                            12:30 AM · 12 Jan
                        </div>

                        <div class="notificationMessage">
                            Admin has started working on this issue.
                        </div>
                    </div>`
}