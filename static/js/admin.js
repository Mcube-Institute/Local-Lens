function getUserIssues() {
    fetch("/issue/getAll?isUser=true")
        .then(res => res.json())
        .then(data => {
            if (data.status == "success") {
               return data.data
            }

            else {
                throw new Error(data.message);
            }
        })
        .catch(err => alert(err.message))
}

function getIssueSpecific(issueId) {
    fetch(`/issue/getSpecific?id=${issueId}`)
        .then(res => res.json())
        .then(data => {
            if (data.status == "success") {
               return data.data
            }

            else {
                throw new Error(data.message);
            }
        })
        .catch(err => alert(err.message))
}

function getUser(userId){
    fetch(`/user/getSpecific?id=${userId}`)
    .then(res=>res.json())
    .then(data=>{
        if(data.message=="success"){
            return data.data
        }
        else{
            throw new Error(data.message);
        }
    })
    .catch(err=>alert(data.message))
}

function getLocation(locationId){
    fetch(`/location/getSpecific?id=${locationId}`)
    .then(res=>res.json())
    .then(data=>{
        if(data.message=="success"){
            return data.data
        }
        else{
            throw new Error(data.message);
        }
    })
    .catch(err=>alert(data.message))
}

function getIssueStatusHistory(issueId){
    fetch(`/status/getAll?id=${issueId}`)
    .then(res=>res.json())
    .then(data=>{
        if(data.message=="success"){
            return data.data
        }
        else{
            throw new Error(data.message);
        }
    })
    .catch(err=>alert(data.message))
}

tableRow=`
    <tr>
                            <td class="sNo">${sNo}</td>

                            <td>
                                <div>
                                    <strong class="name text-nowrap">${user.name}</strong><br>
                                    <small class="text-muted email text-nowrap">${user.email}</small>
                                </div>
                            </td>

                            <td class="issueTittle">${issue.issueTittle}</td>

                            <td class="text-wrap issueDescription" style="max-width:240px;">
                                ${issue.issueDescription}
                            </td>

                            <td class="text-nowrap category" style="max-width:240px;">
                                ${issue.category}
                            </td>

                            <!-- STATUS DROPDOWN -->
                            <td>
                                <select class="form-select form-select-sm statusSelect">
                                    <option value="REPORTED">Reported</option>
                                    <option value="IN_PROGRESS">In Progress</option>
                                    <option value="RESOLVED">Resolved</option>
                                    <option value="CLOSED">Closed</option>
                                </select>
                            </td>

                            <td class="createdAt">12 Jan 2026</td>

                            <td class="address">
                                <span class="street">2-West Car Street,Pudukkudi</span>,
                                <span class="city">Tirunelveli</span><br> ,
                                <span class="state">India</span> -
                                <span class="pincode">627417</span>
                            </td>

                            <!-- HISTORY -->
                            <td class="text-center issueSatausHistory">
                                <button class="btn btn-outline-secondary btn-sm" data-bs-toggle="offcanvas"
                                    data-bs-target="#statusHistoryCanvas">
                                    <i class="bi bi-clock-history"></i>
                                </button>
                            </td>

                            <!-- ATTACHMENTS -->
                            <td class="text-center Attachments">
                                <button class="btn btn-outline-secondary btn-sm" data-bs-toggle="offcanvas"
                                    data-bs-target="#attachmentsCanvas">
                                    <i class="bi bi-paperclip"></i>
                                </button>
                            </td>
                        </tr>
`