async function fetchJSON(url, options = {}) {
    const res = await fetch(url, options);
    const data = await res.json();

    if (data.status !== "success") {
        throw new Error(data.message);
    }
    return data;
}

function formatDate(dt) {
    if (!dt) return "N/A";
    const d = new Date(dt);
    return d.toLocaleDateString("en-Us", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour:"2-digit",
        minute:"2-digit",
        timeZone: "Asia/Kolkata"
    });
}

async function loadRoles() {
    try {
        const res = await fetchJSON("/role/getAll");
        const tbody = $("table tbody");
        tbody.empty();

        let sNo = 1;

        res.data.forEach(role => {
            tbody.append(`
                <tr data-id="${role.id || ''}">
                    <td class="sNo">${sNo++}</td>
                    <td class="role">${role.name}</td>
                    <td class="createdAt">${formatDate(role.createdAt)}</td>
                    <td class="updatedAt">${formatDate(role.updatedAt)}</td>
                    <td class="text-center">
                        <div class="dropdown">
                            <button class="btn btn-sm btn-outline-secondary" data-bs-toggle="dropdown">
                                <i class="bi bi-three-dots-vertical"></i>
                            </button>

                            <ul class="dropdown-menu">
                                <li>
                                    <button class="dropdown-item editRoleBtn">
                                        <i class="bi bi-pencil me-2"></i>Edit
                                    </button>
                                </li>
                                <li>
                                    <button class="dropdown-item text-danger deleteRoleBtn">
                                        <i class="bi bi-trash me-2"></i>Delete
                                    </button>
                                </li>
                            </ul>
                        </div>
                    </td>
                </tr>
            `);
        });

        if (sNo === 1) {
            tbody.append(`
                <tr>
                    <td colspan="5" class="text-center text-muted">
                        No roles found
                    </td>
                </tr>
            `);
        }

    } catch (err) {
        alert(err.message);
    }
}


$("#createRoleBtn").on("click", async function () {
    const roleName = $("#roleName").val().trim();

    if (!roleName) {
        alert("Role name is required");
        return;
    }

    try {
        await fetchJSON("/role/new", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: roleName })
        });

        $("#roleName").val("");
        $("#newRoleModal").modal("hide");

        alert("Role created successfully");
        loadRoles();

    } catch (err) {
        alert(err.message);
    }
});


$(document).on("click", ".editRoleBtn", function () {
    const row = $(this).closest("tr");
    const roleName = row.find(".role").text();

    const newName = prompt("Edit role name", roleName);
    if (!newName || newName.trim() === roleName) return;

    updateRole(row.data("id"), newName.trim());
});

async function updateRole(roleId, name) {
    try {
        await fetchJSON(`/role/update?id=${roleId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name })
        });

        alert("Role updated successfully");
        loadRoles();

    } catch (err) {
        alert(err.message);
    }
}



$(document).on("click", ".deleteRoleBtn", function () {
    const row = $(this).closest("tr");
    const roleName = row.find(".role").text();
    const roleId = row.data("id");

    if (!confirm(`Delete role "${roleName}"?`)) return;

    deleteRole(roleId);
});

async function deleteRole(roleId) {
    try {
        await fetchJSON(`/role/delete?id=${roleId}`, {
            method: "DELETE"
        });

        alert("Role deleted successfully");
        loadRoles();

    } catch (err) {
        alert(err.message);
    }
}

$(document).ready(loadRoles);
