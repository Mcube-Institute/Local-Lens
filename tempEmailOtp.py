from flask import Blueprint,request,jsonify
from models import TempEmailOtp,User
from flask_mail import Message
from flask import current_app
import random
from datetime import datetime,timedelta

def genOtp():
    return (str(random.randint(100000,999999)))

tempEmailOtpBp=Blueprint('tempEmailOtpBp',__name__)

@tempEmailOtpBp.post('/tempEmailOtp/genOtp')
def generateOtp():
    try:
        data=request.get_json()

        email=data.get('email')
        otp=genOtp()

        if not email:
            return jsonify({'status':'error','message':'Email Missing.'}),400

        existing = TempEmailOtp.objects(email=email).first()

        if existing and (datetime.now() - existing.createdAt).seconds < 60:
            return jsonify({
                "status":"error",
                "message":"Please wait 60sec before requesting another OTP."
                    }), 429

        user=User.objects(email=email).first()

        if user:
            return jsonify({'status':'error','message':'Email Address is Already Registered.'}),409
        
        TempEmailOtp.objects(email=email).update_one(
            set__otp=otp,
            set__otpExpiry=datetime.now()+timedelta(minutes=5),
            set__createdAt=datetime.now(),
            upsert=True
                )

        msg=Message(
        "LocalLens Register OTP",
        sender=("LocalLens Support", current_app.config['MAIL_USERNAME']),
        recipients=[email]
        )
        msg.body = f"Thanks For Choosing LocalLens,Your OTP For Register New Account was {otp}. It Will Expires In 5 Minutes."
        current_app.extensions['mail'].send(msg)

        return jsonify({'status':'success','message':'OTP Sent Successfully.'}),200

    except Exception as e:
        return jsonify({'status':'error','message':f'Error {str(e)}'}),500

@tempEmailOtpBp.post('/tempEmailOtp/otpVerification')
def verifyOtp():
    try:
        data=request.get_json()

        email=data.get('email')
        otp=data.get("otp")

        if not email or not otp:
            return jsonify({"status": "error", "message": "Email Or OTP Missing From Server."}), 400

        temp=TempEmailOtp.objects(email=email).order_by('-otpExpiry').first()
        
        if not temp:
                return jsonify({"status":"error","message":"Email Was Not Found."}), 404
        
        if temp.otp != otp:
            return jsonify({"status":"error","message":"Invalid OTP"}),400

        if datetime.now() > temp.otpExpiry:
            return jsonify({'status':'error',"message": "OTP expired"}), 400

        temp.delete()

        return jsonify({"status":"success","message":"OTP Verified Successfully."}),200
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}),500