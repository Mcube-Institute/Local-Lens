from flask import Blueprint,request,jsonify
from models import Issue,User,Location,Role

issueBp=Blueprint("issueBp",__name__)

def getNextAdmin():
    adminRole = Role.objects(name="admin").first()
    admins = User.objects(role=adminRole)

    if not admins:
        return jsonify({"status":"error","message":"Admin Not Found."})

    current = User.objects(role=adminRole, lastAssigned=True).first()

    if not current:
        first = admins.first()
        first.lastAssigned = True
        first.save()
        return first

    adminList = list(admins)
    index = adminList.index(current)

    nextIndex = (index + 1) % len(adminList)
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
            return jsonify({"status":"error","message":"All Fields Required."})
        
        issueTitle=issue.get("issueTittle")
        issueDescription=issue.get("issueDescription")
        category=issue.get("category")
        imagePath=issue.get("imagePath")
        tags=issue.get("tags")

        userId = request.args.get("userId")

        if not userId:
            return jsonify({"status": "error", "message": "userId is required."})
        
        user=User.objects(id=userId).first()

        if not user:
            return jsonify({"status":"error","message":"User Not Found."})

        assignedTo=getNextAdmin()

        if not assignedTo:
            return jsonify({"status":"error","message":"No Admin Available."})    

        if not user:
            return jsonify({"status":"error","message":"User Not Found."})
        
        locationId = request.args.get("locationId")

        if not locationId:
            return jsonify({"status": "error", "message": "locationId is required."})
        
        location=Location.objects(id=locationId).first()

        if not location:
            return jsonify({"status":"error","message":"All Fields Required."})
        
        Location.objects(
            user=user,
            issueTitle=issueTitle,
            issueDescription=issueDescription,
            category=category,
            location=location,
            imagePath=imagePath,
            tags=tags,
            assignedTo=assignedTo
        ).save()

        return jsonify({"status":"success","message":"Issue Created Successfully."})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})
    
@issueBp.get("/issue/getAll")
def allIssues():
    try:
        issues=Issue.objects()

        if not issues:
            return jsonify({"status":"error","message":"Issues Are Empty."})
        
        issueList=[]

        for issue in issues:
            data={
                "user":issue.name.id,
                "issueTittle" :issue.issueTitle,
                "issueDescription":issue.issueDescription,
                "category":issue.category,
                "location":issue.location,
                "imagePath":issue.imagePath,
                "status":issue.status,
                "assignedTo":issue.assignedTo,
                "createdAt":issue.createdAt
            }

            issueList.append(data)

        return jsonify({"status":"success","message":"Issues Are Retrievd Successfully.","data":issueList})            
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})

@issueBp.get("/issue/getspecific")
def issueSpecific():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."})
        
        issue=Issue.objects(id=id).first()

        if not issue:
            return jsonify({"status":"error","message":"Issue Not Found."})
        
        data={
                "user":issue.name.id,
                "issueTittle" :issue.issueTitle,
                "issueDescription":issue.issueDescription,
                "category":issue.category,
                "location":issue.location,
                "imagePath":issue.imagePath,
                "status":issue.status,
                "assignedTo":issue.assignedTo,
                "createdAt":issue.createdAt
            }
        
        return jsonify({"status":"success","message":"Issue Retrieved Successfully.","data":data})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})
    
    
@issueBp.post("/issue/update")
def issueUpdate():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."})
        
        issue=Issue.objects(id=id).first()

        if not issue:
            return jsonify({"status":"error","message":"issue Not Found."})
        
        issueUpdate=request.get_json()

        issueTitle=issueUpdate.get("issueTittle")
        issueDescription=issueUpdate.get("issueDescription")
        category=issueUpdate.get("category")
        imagePath=issueUpdate.get("imagePath")
        tags=issueUpdate.get("tags")

        issue.issueTitle=issueTitle
        issue.Description=issueDescription
        issue.category=category
        issue.imagePath=imagePath
        issue.tags=tags

        return jsonify({"status":"success","message":"Issue Updated Successfully."})
        
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})
    
@issueBp.post("/issue/status")
def issueStatusUpdate():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id Is Required."})
        
        status=request.args.get("status")

        if not status:
            return jsonify({"status": "error", "message": "Status Is Required."})
        
        issue=Issue.objects(id=id).first()

        if not issue:
            return jsonify({"status":"error","message":"issue Not Found."})
        
        issue.status=status

        issue.save()

        return jsonify({"status":"success","message":"Issue's Status Updated Successfully."})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})
    
@issueBp.delete("/issue/delete")
def issueDelete():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id Is Required."}) 
        
        issue=Issue.objects(id=id).first()

        if not issue:
            return jsonify({"status":"error","message":"issue Not Found."})
        
        issue.delete()

        return jsonify({"status":"success","message":"Issue Deleted Successfully."})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})