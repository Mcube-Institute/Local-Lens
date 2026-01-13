from flask import Blueprint,request,jsonify
from  models import User,Role

userBp=Blueprint("userBp",__name__)

@userBp.post("/user/new")
def newUser():
    try:
        user=request.get_json()

        if not user:
            return jsonify({"status":"error","message":"All Fields Required."})
    
        name=user.get("name")
        email=user.get("email")
        password=user.get("password")
        roleId=user.get("roleId")

        if not name or not email or not password or not roleId:
            return jsonify({"status":"error","message":"Missing Fields"})
    
        if User.objects(email=email).first():
            return jsonify({"status":"error","message":"This Email Address Is Already Registered."})
    
        role=Role.objects(id=roleId).first()

        if not role:
            return jsonify({"status":"error","message":"Role Not Found."})
    
        User.objects(
            name=name,
            email=email,
            password=password,
            role=role
        ).save()
    
        return jsonify({"status":"success","message":"User Created Successfully."})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"})
    
@userBp.get("/user/getAll")
def allUsers():
    try:
        users=User.objects()

        if not users:
            return jsonify({"status":"error","message":"Empty Users."})
        
        userList=[]

        for user in users:
            data={
                "name":user.name,
                "email":user.email,
                "password":user.password,
                "role":user.role.name 
            }

            userList.append(data)

        return jsonify({"status":"success","message":"All Users Retrieved.","data":userList})
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"})
    
@userBp.get("/user/getSpecific")
def userSpecific():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."})
        
        user=User.objects(id=id).first()

        if not user:
            return jsonify({"status":"error","message":"User Not Found."})
        
        data={
            "name":user.name,
            "email":user.email,
            "password":user.password,
            "role":user.role.name
        }
        
        return jsonify({"status":"success","message":"All Users Retrieved.","data":data})
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"})
    
@userBp.post("/user/update")
def userUpdate():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."})
        
        user=User.objects(id=id).first()

        if not user:
            return jsonify({"status":"error","message":"User Not Found."})
        
        userData=request.get_json()

        if not userData:
            return jsonify({"status":"error","message":"All Fields Required."})
    
        name=userData.get("name")
        email=userData.get("email")
        password=userData.get("password")
        roleId=userData.get("roleId")

        role=Role.objects(id=roleId).first()

        if not role:
            return jsonify({"status":"error","message":"Role Not Found."})

        user.name=name
        user.email=email
        user.password=password
        user.role=role

        user.save()

        return jsonify({"status":"success","message":"User Updated Successfully."})
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"})
    
@userBp.delete("/user/delete")
def userDelete():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."})

        user=User.objects(id=id).first()

        if not user:
            return jsonify({"status":"error","message":"user Not Found."})
        
        user.delete()

        return({"status":"success","messge":"User Deleted Successfully."})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})