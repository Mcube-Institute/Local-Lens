from flask import Blueprint,request,jsonify
from  models import User,Role,Issue
from issue import getNextAdmin
from notifications import newNotification


userBp=Blueprint("userBp",__name__)

@userBp.post("/user/new")
def newUser():
    try:
        user=request.get_json()

        if not user:
            return jsonify({"status":"error","message":"All Fields Required."}), 400 
    
        name=user.get("name")
        email=user.get("email")
        password=user.get("password")
        roleId=user.get("roleId")

        if not name or not email or not password or not roleId:
            return jsonify({"status":"error","message":"Missing Fields"}), 400
    
        if User.objects(email=email).first():
            return jsonify({"status":"error","message":"This Email Address Is Already Registered."}), 409 
    
        role=Role.objects(id=roleId).first()

        if not role:
            return jsonify({"status":"error","message":"Role Not Found."}), 404 
    
        User(
            name=name,
            email=email,
            password=password,
            role=role
        ).save()
    
        return jsonify({"status":"success","message":"User Created Successfully."}), 201  

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"}), 500
    
@userBp.get("/user/getAll")
def allUsers():
    try:
        users=User.objects()

        if not users:
            return jsonify({"status":"error","message":"Empty Users."}), 200
        
        userList=[]

        for user in users:
            data={
                "name":user.name,
                "email":user.email,
                "password":user.password,
                "role":user.role.name   
            }

            userList.append(data)

        return jsonify({"status":"success","message":"All Users Retrieved.","data":userList}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"}), 500
    
@userBp.get("/user/getSpecific")
def userSpecific():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."}), 400
        
        user=User.objects(id=id).first()

        if not user:
            return jsonify({"status":"error","message":"User Not Found."}), 404
        
        data={
            "name":user.name,
            "email":user.email,
            "password":user.password,
            "role":user.role.name
        }
        
        return jsonify({"status":"success","message":"All Users Retrieved.","data":data}), 200 
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"}), 500
    
@userBp.post("/user/update")
def userUpdate():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."}), 400
        
        user=User.objects(id=id).first()

        if not user:
            return jsonify({"status":"error","message":"User Not Found."}), 404 
        
        userData=request.get_json()

        if not userData:
            return jsonify({"status":"error","message":"All Fields Required."}), 400   
    
        name=userData.get("name")
        email=userData.get("email")
        password=userData.get("password")
        roleId=userData.get("roleId")

        if not name or not email or not roleId:
            return jsonify({
                "status": "error",
                "message": "Name, email and role are required."
            }), 400
        
        if email != user.email and User.objects(email=email).first():
            return jsonify({
                "status": "error",
                "message": "Email already in use."
            }), 409

        role=Role.objects(id=roleId).first()

        if not role:
            return jsonify({"status":"error","message":"Role Not Found."}), 404

        user.name=name
        user.email=email
        user.password=password
        user.role=role

        user.save()

        return jsonify({"status":"success","message":"User Updated Successfully."}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"}), 500
    

@userBp.delete("/user/delete")
def userDelete():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."}), 400

        user = User.objects(id=id).first()

        if not user:
            return jsonify({"status": "error", "message": "User Not Found."}), 404

        adminRole = Role.objects(name="Admin").first()

        if user.role == adminRole:
            
            issues = Issue.objects(assignedTo=user)

            for issue in issues:
                nextAdmin = getNextAdmin()

                if not nextAdmin:
                    return jsonify({
                        "status": "error",
                        "message": "No other admins available to reassign issues."
                    }), 503

                issue.assignedTo = nextAdmin
                issue.save()

                
                newNotification(
                    user=nextAdmin,
                    issue=issue,
                    message=f"Issue reassigned after admin deletion: {issue.issueTittle}"
                )

            
            if user.lastAssigned:
                user.lastAssigned = False
                user.save()
                getNextAdmin()  

        user.delete()

        return jsonify({
            "status": "success",
            "message": "User deleted and issues reassigned successfully."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error {str(e)}"
        }), 500
