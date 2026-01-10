from flask import Blueprint,request,jsonify
from models import Role

roleBp=Blueprint("roleBp",__name__)

@roleBp.post("/role/new")
def newRole():
    try:
        role=request.get_json()

        if not role:
            return jsonify({"status":"error","message":"Role Not To Be Empty."})
        
        name=role.get("name")
        
        Role(
            name=name
        ).save()

        return jsonify({"status": "success", "message": "Role Added Successfully."})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})
    
@roleBp.get("/role/getAll")
def allRoles():
    try:
        roles=Role.objects()

        if not roles:
            return jsonify({"status":"error","message":"Roles Empty."})
        
        roleList=[]

        for role in roles:
            data={
                "name":role.name
            }

            roleList.append(data)

        return jsonify({"status":"success","message":"Roles Are Retrieved Successfully.","data":roleList})

    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})
    
@roleBp.get("/role/getSpecific")
def roleSpecific():
     try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."})
        
        role=Role.objects(id=id).first()

        if not role:
            return jsonify({"status":"error","message":"Role Not Found."})
        
        data={
            "name":role.name
            }

        return jsonify({"status":"success","message":"Role Retrieved Successfully.","data":data})
     
     except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})
     
@roleBp.post("/role/update")
def roleUpdate():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."})    
        
        roleName=request.get_json()

        if not roleName:
            return jsonify({"status":"error","message":"Role Not To Be Empty."})
        
        name=roleName.get("name")

        if Role.objects(name=name).first():
            return jsonify({"status":"error","message":"Duplicated Role."})
        
        role=Role.objects(id=id).first()

        if not role:
            return jsonify({"status":"error","message":"Role Not Found."})

        role.name=name

        role.save()

        return jsonify({"status":"success","message":"Role Updated Successfully."})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})
    
@roleBp.delete("/role/delete")
def roleDelete():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."})

        role=Role.objects(id=id).first()

        if not role:
            return jsonify({"status":"error","message":"Role Not Found."})
        
        role.delete()

        return jsonify({"status":"success","messge":"Role Deleted Successfully."})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})