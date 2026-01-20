from flask import Blueprint,request,jsonify,session
from models import Issue,User,Location,Role,IssueStatusHistory
from datetime import datetime
from notifications import newNotification

issueBp=Blueprint("issueBp",__name__)

def getNextAdmin():
    adminRole = Role.objects(name="Admin").first()
    if not adminRole:
        return None

    admins = User.objects(role=adminRole)
    if not admins:
        return None

    current = User.objects(role=adminRole, lastAssigned=True).first()

    # If no admin was previously assigned, pick first
    if not current:
        first = admins.first()
        first.lastAssigned = True
        first.save()
        return first

    adminList = list(admins)

    # Safety check
    if current not in adminList:
        current.lastAssigned = False
        current.save()
        first = adminList[0]
        first.lastAssigned = True
        first.save()
        return first

    index = adminList.index(current)

    if index == len(adminList)-1:
        current.lastAssigned = False
        current.save()
        first = admins.first()
        first.lastAssigned = True
        first.save()
        return first
    else:
        nextIndex = index + 1

    nextAdmin = adminList[nextIndex]

    current.lastAssigned = False
    current.save()

    nextAdmin.lastAssigned = True
    nextAdmin.save()

    return nextAdmin


@issueBp.post("/issue/new")
def newIssue():
    try:
        issue=request.get_json()

        if not issue:
            return jsonify({"status":"error","message":"All Fields Required."}), 400
        
        issueTittle=issue.get("issueTittle")
        issueDescription=issue.get("issueDescription")
        category=issue.get("category")
        imagePath=issue.get("imagePath")
        tags=issue.get("tags")

        if not issueTittle or not issueDescription or not category:
            return jsonify({
                "status": "error",
                "message": "Issue title, description and category are required."
            }), 400

        userId =session.get("user").get("id")

        if not userId:
            return jsonify({"status": "error", "message": "userId is required."}), 400
        
        user=User.objects(id=userId).first()

        if not user:
            return jsonify({"status":"error","message":"User Not Found."}), 404

        assignedTo=getNextAdmin()

        if not assignedTo:
            return jsonify({"status":"error","message":"No Admin Available."}), 503       

        if not user:
            return jsonify({"status":"error","message":"User Not Found."}), 404
        
        locationId = request.args.get("locationId")

        if not locationId:
            return jsonify({"status": "error", "message": "locationId is required."}), 400
        
        location=Location.objects(id=locationId).first()

        if not location:
            return jsonify({"status":"error","message":"LocationNot Found."}), 404
        
        Issue(
            user=user,
            issueTittle=issueTittle,
            issueDescription=issueDescription,
            category=category,
            location=location,
            imagePath=imagePath,
            tags=tags,
            assignedTo=assignedTo
        ).save()

        newNotification(
            user=assignedTo,
            issue=Issue.objects(user=user).order_by('-createdAt').first(),
            message=f"New Issue Assigned:{issueTittle}"
        )

        return jsonify({"status":"success","message":"Issue Created Successfully."}), 201
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500
    
@issueBp.get("/issue/getAll")
def allIssues():
    try:
        issues=Issue.objects()

        if not issues:
            return jsonify({"status":"error","message":"Issues Are Empty."}), 200
        
        issueList=[]

        for issue in issues:
            data={
                "user": {
                    "id": issue.user.id,
                    "name": issue.user.name,
                    "email": issue.user.email
                    },
                "issueTittle" :issue.issueTittle,
                "issueDescription":issue.issueDescription,
                "category":issue.category,
                "location":issue.location.id,
                "imagePath":issue.imagePath,
                "status":issue.status,
                "assignedTo":issue.assignedTo.id,
                "createdAt":issue.createdAt
            }

            issueList.append(data)

        return jsonify({"status":"success","message":"Issues Are Retrievd Successfully.","data":issueList}), 200           
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500

@issueBp.get("/issue/getSpecific")
def issueSpecific():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."}), 400
        
        issue=Issue.objects(id=id).first()

        if not issue:
            return jsonify({"status":"error","message":"Issue Not Found."}), 404
        
        data={
                "user": {
                    "id": issue.user.id,
                    "name": issue.user.name,
                    "email": issue.user.email
                    },
                "issueTittle" :issue.issueTittle,
                "issueDescription":issue.issueDescription,
                "category":issue.category,
                "location":issue.location.id,
                "imagePath":issue.imagePath,
                "status":issue.status,
                "assignedTo":issue.assignedTo.id,
                "createdAt":issue.createdAt
            }
        
        return jsonify({"status":"success","message":"Issue Retrieved Successfully.","data":data}), 200
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500
    
    
@issueBp.post("/issue/update")
def issueUpdate():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."}), 400
        
        issue=Issue.objects(id=id).first()

        if not issue:
            return jsonify({"status":"error","message":"issue Not Found."}), 404 
        
        issueData = request.get_json()

        if not issueData:
            return jsonify({
                "status": "error",
                "message": "Issue data is required."
            }), 400

        issueTitle=issueData.get("issueTittle")
        issueDescription=issueData.get("issueDescription")
        category=issueData.get("category")
        imagePath=issueData.get("imagePath")
        tags=issueData.get("tags")

        if not issueTitle or not issueDescription or not category:
            return jsonify({
                "status": "error",
                "message": "Issue title, description and category are required."
            }), 400

        issue.issueTitle=issueTitle
        issue.IssueDescription=issueDescription
        issue.category=category
        issue.imagePath=imagePath
        issue.tags=tags

        issue.save()

        return jsonify({"status":"success","message":"Issue Updated Successfully."}), 200 
        
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500
    
@issueBp.post("/issue/status")
def issueStatusUpdate():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id Is Required."}), 400
        
        status=request.args.get("status")

        if not status:
            return jsonify({"status": "error", "message": "Status Is Required."}), 400
        
        allowed_statuses = ["REPORTED", "IN_PROGRESS", "RESOLVED", "CLOSED"]
        if status not in allowed_statuses:
            return jsonify({
                "status": "error",
                "message": f"Invalid status. Allowed: {allowed_statuses}"
            }), 400
        
        rejectedReason=""
        
        if status == "CLOSED":

            reason=request.get_json()

            rejectedReason=reason.get("rejectedReason")

        resolvedAt=""

        if status == "RESOLVED":
            resolvedAt=datetime.now()
        
        issue=Issue.objects(id=id).first()

        if not issue:
            return jsonify({"status":"error","message":"issue Not Found."}), 404
        
        userId=session.get("user").get("id")

        if not userId:
            return jsonify({"status": "error", "message": "userId is required."}), 400

        if not userId==issue.assignedTo.id:
            return jsonify({"status":"error","message":"Only Assigned Admin Can Edit IssueStatus."})
        
        updatedBy=User.objects(id=userId).first()

        if not updatedBy:
            return jsonify({"status":"error","message":"User Not Found."}), 404
        
        prevStatus=issue.status
        
        issue.status=status

        issue.save()
        
        IssueStatusHistory(
            issue=id,
            prevStatus=prevStatus,
            nextStatus=status,
            updatedBy=updatedBy.id,
            rejectedReason=rejectedReason or None,
            resolvedAt=resolvedAt or None
        ).save()

        if status == "IN_PROGRESS":
            newNotification(
                user=issue.user.id,
                issue=issue,
                message=f"Your Issue Is Now {status}."
            )

        elif status == "RESOLVED":
            newNotification(
                user=issue.user.id,
                issue=issue,
                message=f"Your Issue Has Been {status}."
            )

        elif status == "CLOSED":
            newNotification(
                user=issue.user.id,
                issue=issue,
                message=f"Your Issue Has Been {status}:{rejectedReason}."
            )

        return jsonify({"status":"success","message":"Issue's Status Updated Successfully."}), 200
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500
    
@issueBp.delete("/issue/delete")
def issueDelete():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id Is Required."}), 400 
        
        issue=Issue.objects(id=id).first()

        if not issue:
            return jsonify({"status":"error","message":"issue Not Found."}), 404
        
        issue.delete()

        return jsonify({"status":"success","message":"Issue Deleted Successfully."}), 200
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500