from flask import Blueprint,request,jsonify,session,redirect
from models import User

authBp=Blueprint("authBp",__name__)

@authBp.post("/auth/register")
def register():
    try:
        userCredentials=request.get_json()

        if not userCredentials:
            return jsonify({"status":"error","message":"All Fields Required."}), 400
        
        name=userCredentials.get("name")
        email=userCredentials.get("email")
        password=userCredentials.get("password")

        if not name and not email and not password:
            return jsonify({"status":"error","message":"Missing Fields"}), 400 

        if User.objects(email=email).first():
            return jsonify({"status":"error","message":"This Email Address Is Already Registered."}), 409 
        
        user=User(
            name=name,
            email=email,
            password=password
        ).save()

        session["user"]={
            "id":user.id,
            "name":name,
            "email":email
        }
 
        return jsonify({"status": "success", "message": "User Registered Successfully."}), 201   
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"}), 500
    
@authBp.post("/auth/logIn")
def login():
    try:
        userCredentials=request.get_json()

        if not userCredentials:
            return jsonify({"status": "error", "message": "All Fields Required."}) , 400 
        
        email=userCredentials.get("email")
        password=userCredentials.get("password")

        if not email or not password:
            return jsonify({
                "status": "error",
                "message": "Email and password are required."
            }), 400
        
        user = User.objects(email=email,password=password).first()

        if not user:
            return jsonify({"status": "error", "message": "Invalid Email or Password."}), 401
        
        session["user"]={
            "id":user.id,
            "name":user.name,
            "email":user.email
        }

        return jsonify({"status": "success", "message": "Loggedin Successfully."}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"}),500
    
@authBp.get("/auth/logOut")
def logOut():
    
    session.clear()

    return redirect("/")