from flask import Blueprint,request,jsonify
from models import Role

roleBp=Blueprint("roleBp",__name__)

@roleBp.post("/role/new")
def newRole():
    try:
        role=request.get_json()

        if not role:
            return jsonify({"status":"error","message":"Role Not To Be Empty."}), 400
        
        name=role.get("name")

        if not name:
            return jsonify({
                "status": "error",
                "message": "Role name is required."
            }), 400
        
        if Role.objects(name=name).first():
            return jsonify({
                "status": "error",
                "message": "Role already exists."
            }), 409
        
        Role(
            name=name
        ).save()

        return jsonify({"status": "success", "message": "Role Added Successfully."}), 201
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500
    
@roleBp.get("/role/getAll")
def allRoles():
    try:
        roles=Role.objects()

        if not roles:
            return jsonify({"status":"error","message":"Roles Empty."}), 200
        
        roleList=[]

        for role in roles:
            data={
                "name":role.name
            }

            roleList.append(data)

        return jsonify({"status":"success","message":"Roles Are Retrieved Successfully.","data":roleList}), 200

    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500
    
@roleBp.get("/role/getSpecific")
def roleSpecific():
     try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."}), 400 
        
        role=Role.objects(id=id).first()

        if not role:
            return jsonify({"status":"error","message":"Role Not Found."}), 404 
        
        data={
            "name":role.name
            }

        return jsonify({"status":"success","message":"Role Retrieved Successfully.","data":data}), 200
     
     except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500 
     
@roleBp.post("/role/update")
def roleUpdate():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."}), 400     
        
        roleName=request.get_json()

        if not roleName:
            return jsonify({"status":"error","message":"Role Not To Be Empty."}), 400  
        
        name=roleName.get("name")

        if not name:
            return jsonify({
                "status": "error",
                "message": "Role name is required."
            }), 400

        if Role.objects(name=name).first():
            return jsonify({"status":"error","message":"Duplicated Role."}), 409
        
        role=Role.objects(id=id).first()

        if not role:
            return jsonify({"status":"error","message":"Role Not Found."}), 404 

        role.name=name

        role.save()

        return jsonify({"status":"success","message":"Role Updated Successfully."}), 200 
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500
    
@roleBp.delete("/role/delete")
def roleDelete():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."}), 400  

        role=Role.objects(id=id).first()

        if not role:
            return jsonify({"status":"error","message":"Role Not Found."}), 404 
        
        role.delete()

        return jsonify({"status":"success","messge":"Role Deleted Successfully."}), 200 
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500