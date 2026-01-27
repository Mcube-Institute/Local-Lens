from flask import Blueprint,request,jsonify,session
from models import Notifications
from datetime import datetime

notificationBp=Blueprint("notificatiosBp",__name__)

def newNotification(user,issue,message):
    Notifications(
        user=user,
        issue=issue,
        message=message,
        updatedAt=datetime.now()
    ).save()

@notificationBp.get("/notification/getAll")
def getNotications():
    try:
        currentUser = session.get("user")
        if not currentUser:
            return jsonify({"status":"error","message":"Login required"}), 401

        userId = currentUser["id"]
        
        notifications=Notifications.objects(user=userId).order_by("-updatedAt")

        notificationList=[]

        for notification in notifications:
            data={
                "id": notification.id,
                "issue": notification.issue.id,
                "message": notification.message,
                "isViewed": notification.isViewed,
                "createdAt": notification.createdAt
            }
            
            notificationList.append(data)

        return jsonify({"status":"success","message":"Notifications Retrieved Successfully.","data":notificationList}), 200
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}) ,500
    
@notificationBp.post("/notification/view")
def notificationViewed():
    try:
        notificationId = request.args.get("id")

        if not notificationId:
            return jsonify({"status": "error", "message": "Id Required"}), 400

        notification = Notifications.objects(id=notificationId).first()

        if not notification:
            return jsonify({"status": "error", "message": "Notification Not Found"}), 404

        notification.isViewed = True
        notification.save()

        return jsonify({
            "status": "success",
            "message": "Notification marked as viewed."
        }), 200
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})