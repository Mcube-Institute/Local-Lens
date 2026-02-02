async function fetchJSON(url, options = {}) {
    const res = await fetch(url, options);
    const data = await res.json();

    if (data.status !== "success") {
        throw new Error(data.message);
    }
    return data;
}

let roleList = [];

async function loadRoles() {
    const res = await fetchJSON("/role/getAll");
    roleList = res.data;

    const roleSelect = $("#userRole");
    roleSelect.empty();

    roleList.forEach(role => {
        roleSelect.append(`
            <option value="${role.name}">${role.name}</option>
        `);
    });
}

async function loadUsers() {
    try {
        const res = await fetchJSON("/user/getAll");
        const tbody = $("table tbody");
        tbody.empty();

        let sNo = 1;

        res.data.forEach(user => {
            tbody.append(`
                <tr data-id="${user.id}">
                    <td>${sNo++}</td>
                    <td class="name">${user.name}</td>
                    <td class="email">${user.email}</td>
                    <td>
                        <select class="form-select form-select-sm roleSelect">
                            ${renderRoleOptions(user.role)}
                        </select>
                    </td>
                    <td class="text-center">
                        <div class="dropdown">
                            <button class="btn btn-sm btn-outline-secondary" data-bs-toggle="dropdown">
                                <i class="bi bi-three-dots-vertical"></i>
                            </button>
                            <ul class="dropdown-menu">
                                <li>
                                    <button class="dropdown-item deleteUserBtn text-danger">
                                        <i class="bi bi-trash me-2"></i>Delete
                                    </button>
                                </li>
                            </ul>
                        </div>
                    </td>
                </tr>
            `);
        });

    } catch (err) {
        alert(err.message);
    }
}

function renderRoleOptions(selectedRole) {
    return roleList.map(role => `
        <option value="${role.name}" ${role.name === selectedRole ? "selected" : ""}>
            ${role.name}
        </option>
    `).join("");
}


$(document).on("change", ".roleSelect", async function () {
    const select = $(this);
    const row = select.closest("tr");

    const userId = row.data("id");
    const role = select.val();

    try {
        await fetchJSON(`/user/update?id=${userId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: row.find(".name").text(),
                email: row.find(".email").text(),
                role: role
            })
        });

        alert("User role updated");

    } catch (err) {
        alert(err.message);
        loadUsers(); 
    }
});

$("#createUserBtn").on("click", async function () {
    const name = $("#name").val().trim();
    const email = $("#email").val().trim();
    const password = $("#password").val();
    const role = $("#userRole").val();

    if (!name || !email || !password || !role) {
        alert("All fields required");
        return;
    }

    try {
        await fetchJSON("/user/new", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password, role })
        });

        $("#newUserModal").modal("hide");
        $("#name, #email, #password").val("");

        alert("User created");
        loadUsers();

    } catch (err) {
        alert(err.message);
    }
});

$(document).on("click", ".deleteUserBtn", async function () {
    const row = $(this).closest("tr");
    const userId = row.data("id");
    const name = row.find(".name").text();

    if (!confirm(`Delete user "${name}"?`)) return;

    try {
        await fetchJSON(`/user/delete?id=${userId}`, {
            method: "DELETE"
        });

        alert("User deleted");
        loadUsers();

    } catch (err) {
        alert(err.message);
    }
});

$(document).ready(async function () {
    await loadRoles();
    loadUsers();
});
