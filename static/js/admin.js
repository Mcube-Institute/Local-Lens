
const CURRENT_USER = window.APP_USER;

if (!CURRENT_USER || !CURRENT_USER.isLogIn) {
    alert("Session expired. Please login again.");
    window.location.href = "/login";
}

const CURRENT_ADMIN_ID = CURRENT_USER.id;


async function fetchJSON(url, options = {}) {
    const res = await fetch(url, options);
    const data = await res.json();
    if (data.status !== "success") {
        throw new Error(data.message);
    }
    return data;
}

function formatDate(dt) {
    if (!dt) return "-";
    const d = new Date(dt);
    return d.toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric"
    });
}

function formatLocation(loc) {
    if (!loc) return "-";
    return `${loc.street}, ${loc.city}, ${loc.state} - ${loc.pincode}`;
}


async function loadAdminIssues() {
    try {
        const res = await fetchJSON("/issue/getAll");
        const tbody = $("#adminIssueTable");
        tbody.empty();

        let sNo = 1;

        for (const issue of res.data) {

            if (issue.assignedTo !== CURRENT_ADMIN_ID) continue;

            let locationText = "-";
            try {
                const locRes = await fetchJSON(`/location/getSpecific?id=${issue.location}`);
                locationText = formatLocation(locRes.data);
            } catch {
                locationText = "-";
            }

            tbody.append(`
                <tr data-id="${issue.id}" data-status="${issue.status}">
                    <td>${sNo++}</td>

                    <td>
                        <strong>${issue.user.name}</strong><br>
                        <small class="text-muted">${issue.user.email}</small>
                    </td>

                    <td>${issue.issueTittle}</td>

                    <td class="text-wrap" style="max-width:240px;">
                        ${issue.issueDescription}
                    </td>

                    <td>${issue.category}</td>

                    <td>
                        <select class="form-select form-select-sm statusSelect">
                            <option value="REPORTED" ${issue.status === "REPORTED" ? "selected" : ""}>Reported</option>
                            <option value="IN_PROGRESS" ${issue.status === "IN_PROGRESS" ? "selected" : ""}>In Progress</option>
                            <option value="RESOLVED" ${issue.status === "RESOLVED" ? "selected" : ""}>Resolved</option>
                            <option value="CLOSED" ${issue.status === "CLOSED" ? "selected" : ""}>Closed</option>
                        </select>
                    </td>

                    <td>${formatDate(issue.createdAt)}</td>

                    <td class="text-wrap" style="max-width:220px;">
                        ${locationText}
                    </td>

                    <td class="text-center">
                        <button class="btn btn-sm btn-outline-secondary viewHistory">
                            <i class="bi bi-clock-history"></i>
                        </button>
                    </td>

                    <td class="text-center">
                        <button class="btn btn-sm btn-outline-secondary viewAttachments">
                            <i class="bi bi-paperclip"></i>
                        </button>
                    </td>
                </tr>
            `);
        }

        if (sNo === 1) {
            tbody.append(`
                <tr>
                    <td colspan="10" class="text-center text-muted">
                        No issues assigned to you
                    </td>
                </tr>
            `);
        }

    } catch (err) {
        alert(err.message);
    }
}


$(document).on("change", ".statusSelect", async function () {
    const select = $(this);
    const row = select.closest("tr");

    const issueId = row.data("id");
    const oldStatus = row.data("status");
    const newStatus = select.val();

    let body = null;
    let headers = {};

    if (newStatus === "CLOSED") {
        const reason = prompt("Enter rejection reason");
        if (!reason) {
            select.val(oldStatus); // revert
            return;
        }
        body = JSON.stringify({ rejectedReason: reason });
        headers["Content-Type"] = "application/json";
    }

    try {
        const res = await fetch(`/issue/status?id=${issueId}&status=${newStatus}`, {
            method: "POST",
            headers,
            body
        });

        const data = await res.json();

        if (data.status !== "success") {
            throw new Error(data.message);
        }

        alert("Status updated successfully");

        // persist new status
        row.attr("data-status", newStatus);

    } catch (err) {
        alert(err.message);
        select.val(oldStatus); // revert UI
    }
});


$(document).on("click", ".viewHistory", async function () {
    const issueId = $(this).closest("tr").data("id");
    const list = $("#statusHistoryCanvas .list-group");
    list.empty();

    try {
        const res = await fetchJSON(`/status/getAll?id=${issueId}`);

        res.data.forEach(h => {
            list.append(`
                <li class="list-group-item">
                    <strong>${h.prevStatus}</strong>
                    <i class="bi bi-arrow-right"></i>
                    <strong>${h.nextStatus}</strong><br>
                    ${h.rejectedReason ? `<small>${h.rejectedReason}</small><br>` : ""}
                    <small class="text-muted">
                        ${h.resolvedAt ? "Resolved: " + formatDate(h.resolvedAt) : formatDate(h.createdAt)}
                    </small>
                </li>
            `);
        });

        bootstrap.Offcanvas
            .getOrCreateInstance(document.getElementById("statusHistoryCanvas"))
            .show();

    } catch (err) {
        alert(err.message);
    }
});


$(document).on("click", ".viewAttachments", async function () {
    const issueId = $(this).closest("tr").data("id");
    const body = $("#attachmentsCanvas .offcanvas-body");
    body.empty();

    try {
        const res = await fetchJSON(`/issue/getSpecific?id=${issueId}`);
        const files = res.data.imagePath;

        if (!files || files.length === 0) {
            body.html("<p class='text-muted'>No attachments</p>");
        }

        files.forEach(file => {
            const ext = file.split(".").pop().toLowerCase();

            if (["jpg", "jpeg", "png", "webp", "gif"].includes(ext)) {
                body.append(`<img src="${file}" class="img-fluid rounded mb-2">`);
            } else if (["mp4", "webm", "ogg"].includes(ext)) {
                body.append(`
                    <video controls class="w-100 rounded mb-2">
                        <source src="${file}">
                    </video>
                `);
            }
        });

        bootstrap.Offcanvas
            .getOrCreateInstance(document.getElementById("attachmentsCanvas"))
            .show();

    } catch (err) {
        alert(err.message);
    }
});

$(document).ready(loadAdminIssues);
