from flask import Blueprint,request,jsonify,session,redirect
from models import User
import random
from flask_mail import Message
from flask import current_app
from datetime import datetime,timedelta

def genOtp():
    return(str(random.randint(100000,999999)))

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

@authBp.post("/auth/forgetPassword")
def forgetPassword():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"status":"error","message":"All Fields Are Required."}), 400

        email=data.get('email')

        if not email:
            return jsonify({"status": "error", "message": "Email is required."}), 400
        
        user=User.objects(email=email).first()

        if not user:
            return jsonify({"status":"error","message":"User Not Found."}), 404

        otp=genOtp()            
        user.otp=otp
        user.otpExpiry=datetime.now()+timedelta(minutes=5)
        user.save()

        msg=Message(
        "Password Reset OTP",
        sender=("LocalLens Support", current_app.config['MAIL_USERNAME']),
        recipients=[email]
        )
        msg.body = f"Thanks For Using LocalLens,Your OTP For Password Reset {otp}. It Will Expires In 5 Minutes."
        current_app.extensions['mail'].send(msg)
        
        return jsonify({"status":"success","message":"OTP Sent Successfully."}), 200 
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {str(e)}"}), 500

@authBp.post("/auth/otpVerification")        
def verifyOtp():
    try:
        data=request.get_json()
        if not data:
            return jsonify({"status":"error","message":"All Fields Are Required."}), 400

        email=data.get('email')
        otp=data.get("otp")

        if not email or not otp:
            return jsonify({"status": "error", "message": "Email Or OTP Missing From Server."}), 400

        user=User.objects(email=email).first()
        if not user:
                return jsonify({"status":"error","message":"Email Was Not Registered,Please Register."}), 404
        
        if user.otp != otp:
            return jsonify({"status":"error","message":"Invalid OTP"}),400

        if datetime.now() > user.otpExpiry:
            return jsonify({"message": "OTP expired"}), 400

        user.otp=None
        user.otpExpiry=None
        user.save()

        return jsonify({"status":"success","message":"OTP Verified Successfully."}),200
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}),500

    
@authBp.get("/auth/logOut")
def logOut():
    
    session.clear()

    return redirect("/")