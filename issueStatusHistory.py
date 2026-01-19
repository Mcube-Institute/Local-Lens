from flask import Blueprint,request,jsonify
from models import Issue,IssueStatusHistory

statusBp=Blueprint("statusBp",__name__)
    
@statusBp.get("/status/getAll")
def issueSatatusHistoryAll():
    try:
        id=request.args.get("id")

        if not id:
            return jsonify({"status":"error","message":"Id Is Required."}), 400
        
        issue=Issue.objects(id=id).first()

        if not issue:
            return jsonify({"status":"error","message":"Issue Not Found."}), 404
        
        issueStatusHistory=IssueStatusHistory.objects(issue=issue)

        issueStatusHistoryList=[]

        for issueStatus in issueStatusHistory:
            data={
                "issue":issueStatus.issue.id,
                "prevStatus":issueStatus.prevStatus,
                "nextStatus":issueStatus.nextStatus,
                "updatedBy":{
                    "id": issue.user.id,
                    "name": issue.user.name,
                    "email": issue.user.email
                },
                "rejectedReason":issueStatus.rejectedReason,
                "resolvedAt":issueStatus.resolvedAt
            }

            issueStatusHistoryList.append(data)

        return jsonify({"status":"success","message":"Issue Status History Retrieved Successfully.","data":issueStatusHistoryList}), 200
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500