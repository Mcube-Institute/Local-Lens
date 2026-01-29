from flask import Blueprint,request,jsonify,session
from models import Issue,User,Location,Role,IssueStatusHistory
from datetime import datetime
from notifications import newNotification
import base64

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

import os
import uuid
UPLOAD_FOLDER = "static/uploads/issues"

@issueBp.post("/issue/new")
def newIssue():
    try:
        issue=request.form
        print(issue)

        if not issue:
            return jsonify({"status":"error","message":"All Fields Required."}), 400
        
        issueTittle=issue.get("issueTittle")
        issueDescription=issue.get("issueDescription")
        category=issue.get("category")
        tags=issue.get("tags")

        if not issueTittle or not issueDescription or not category:
            return jsonify({
                "status": "error",
                "message": "Issue title, description and category are required."
            }), 400
        
        attachments=request.files.getlist("attachments")
        if not attachments:
            return jsonify({"status": "error", "message": "No files uploaded"}), 400

        result = []

        # for file in attachments:
        #     binary_data = file.read()
        #     base64_data = base64.b64encode(binary_data).decode("utf-8")

        #     data_url = f"data:{file.content_type};base64,{base64_data}"
        #     result.append(data_url)

        for file in attachments:
            ext = file.filename.rsplit(".", 1)[-1]
            filename = f"{uuid.uuid4()}.{ext}"

            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)

            file_url = f"/static/uploads/issues/{filename}"
            result.append(file_url)



        currentUser = session.get("user")
        if not currentUser:
            return jsonify({"status":"error","message":"Login required"}), 401

        userId = currentUser["id"]

        
        user=User.objects(id=userId).first()

        if not user:
            return jsonify({"status":"error","message":"User Not Found."}), 404

        assignedTo=getNextAdmin()

        if not assignedTo:
            return jsonify({"status":"error","message":"No Admin Available."}), 503       

        if not user:
            return jsonify({"status":"error","message":"User Not Found."}), 404
        
        locationId = issue.get("locationId")
        if not locationId:
            return jsonify({"status":"error","message":"locationId is required"}),400
        
        location=Location.objects(id=locationId).first()

        if not location:
            return jsonify({"status":"error","message":"LocationNot Found."}), 404
        
        Issue(
            user=user,
            issueTittle=issueTittle,
            issueDescription=issueDescription,
            category=category,
            location=location,
            attachments=result,
            tags=tags,
            assignedTo=assignedTo
        ).save()

        newNotification(
            user=user,
            issue=Issue.objects(user=user).order_by('-createdAt').first(),
            message=f"Issue Reported:{issueTittle}"
        )

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
        isUser = request.args.get("isUser")
        
        currentUser = session.get("user")
        userId = currentUser["id"]
        
        user=User.objects(id=userId).first()
        if not user:
            return jsonify({"status":"error","message":"User Not Found."}), 404
        
        if isUser:
            issues=Issue.objects(user=user)
        else:
            issues=Issue.objects()
        
        issues = issues.order_by("-createdAt")

        issueList=[]

        for issue in issues:
            data={
                "id": issue.id,
                "user": {
                    "id": issue.user.id,
                    "name": issue.user.name,
                    "email": issue.user.email
                    },
                "issueTittle" :issue.issueTittle,
                "issueDescription":issue.issueDescription,
                "category":issue.category,
                "location":issue.location.id,
                "imagePath":issue.attachments,
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
                "imagePath":issue.attachments,
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
        
        currentUser = session.get("user")
        if not currentUser:
            return jsonify({"status":"error","message":"Login required"}), 401

        userId = currentUser["id"]

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