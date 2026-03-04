from flask import Flask,request,render_template,jsonify,session,redirect
import os
from dotenv import load_dotenv
from flask_mail import Mail,Message
from mongoengine import connect,connection
from models import *
from auth import authBp
from role import roleBp
from user import userBp
from issue import issueBp
from location import locationBp
from issueStatusHistory import statusBp
from notifications import notificationBp
from tempEmailOtp import tempEmailOtpBp

app=Flask(__name__)

load_dotenv("secret.env")


app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT",587))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
print("MAIL CONFIG:", app.config["MAIL_SERVER"], app.config["MAIL_PORT"])

try:
    connect(host=os.getenv("MONGO_URI"))
    if connection.get_connection():
        print("Atlas Database Connected.")
    else:
        print("Database not connected.")
except Exception as e:
    print(f"Error: {str(e)}")

app.register_blueprint(authBp)
app.register_blueprint(roleBp)
app.register_blueprint(userBp)
app.register_blueprint(issueBp)
app.register_blueprint(locationBp)
app.register_blueprint(statusBp)
app.register_blueprint(notificationBp)
app.register_blueprint(tempEmailOtpBp)

@app.get("/")
def home():
    # if not session.get("user"):
    #     return redirect("/login")
    return render_template("index.html")

@app.get("/admin")
def admin():
    return render_template("/admin/admin.html")

@app.get("/super/<page>")
def superAdmin(page):
    return render_template(f"/superAdmin/{page}.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")    

@app.route("/resetPassword")
def resetPassword():
    return render_template("forgetPassword.html")   

@app.route("/mail-test")
def mail_test():
    msg = Message(
        subject="Test Email",
        sender=app.config["MAIL_USERNAME"],
        recipients=["thalathanush8@gmail.com"]
    )
    msg.body = "Mail test from Render"
    mail.send(msg)
    return "Mail sent" 

@app.context_processor
def loadData():
    isLogIn=True
    sessionUser = session.get("user")

    if not sessionUser:
        isLogIn=False
        return {"isLogIn":isLogIn}

    userId = sessionUser["id"]
    user=User.objects(id=userId).first()

    if not user:
        return jsonify({"status":"error","message":"User Not Found."}), 404
    
    userData={
        "id":str(user.id),
        "name":user.name,
        "email":user.email,
        "password":user.password,
        "role": user.role.name,
        "isLogIn":isLogIn
    }
    return userData

mail = Mail(app)


if __name__=="__main__":
    app.run(debug=True)