from flask import Blueprint,request,jsonify
from models import User

authBp=Blueprint("authBp",__name__)

@authBp.post("/auth/register")
def register():
    try:
        userCredentials=request.get_json()

        if not userCredentials:
            return jsonify({"status":"error","message":"All Fields Required."})
        
        name=userCredentials.get("name")
        email=userCredentials.get("email")
        password=userCredentials.get("password")

        if not name and not email and not password:
            return jsonify({"status":"error","message":"Missing Fields"})

        if User.objects(email=email).first():
            return jsonify({"status":"error","message":"This Email Address Is Already Registered."})
        
        User(
            name=name,
            email=email,
            password=password
        ).save()
 
        return jsonify({"status": "success", "message": "User Registered Successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"})
    
@authBp.post("/auth/logIn")
def login():
    try:
        userCredentials=request.get_json()

        if not userCredentials:
            return jsonify({"status": "error", "message": "All Fields Required."}) 
        
        email=userCredentials.get("email")
        password=userCredentials.get("password")
        
        user = User.objects(email=email,password=password).first()

        if not user:
            return jsonify({"status": "error", "message": "Invalid Email or Password."})

        return jsonify({"status": "success", "message": "Loggedin Successfully."})
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"})
    
@authBp.get("/auth/logOut")
def logOut():
    return jsonify({"status":"success","message":"Logged Out"})