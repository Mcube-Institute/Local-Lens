from flask import Blueprint,request,jsonify
from models import User

authBp=Blueprint("authBp",__name__)

@authBp.post("/auth/register")
def register():
    try:
        userCredentials=request.get_json()

        if not userCredentials:
            return jsonify({"status":"error","message":"All fields required."})
        
        name=userCredentials.get("name")
        email=userCredentials.get("email")
        password=userCredentials.get("password")

        if not name or not email or not password:
            return jsonify({"status":"error","message":"Missing fields"})

        if User.objects(email=email).first():
            return jsonify({"status":"error","message":"This email address is already registered."})
        
        user=User(
            name=name,
            email=email,
            password=password
        ).save()
 
        return jsonify({"status": "success", "message": "User created successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"})
    
@authBp.post("/auth/logIn")
def login():
    try:
        userCredentials=request.get_json()

        if not userCredentials:
            return jsonify({"status": "error", "message": "All fields required."}) 
        
        email=userCredentials.get("email")
        password=userCredentials.get("password")
        
        user = User.objects(email=email,password=password).first()

        if not user:
            return jsonify({"status": "error", "message": "Invalid email or password."})

        return jsonify({"status": "success", "message": "Loggedin successfully.","isAuth": True})
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"})
    
@authBp.get("/auth/logOut")
def logOut():
    return jsonify({"status":"success","message":"Logged out"})