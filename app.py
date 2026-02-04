from flask import Flask,request,render_template,jsonify,session,redirect
from mongoengine import connect,connection
from models import *
from auth import authBp
from role import roleBp
from user import userBp
from issue import issueBp
from location import locationBp
from issueStatusHistory import statusBp
from notifications import notificationBp

app=Flask(__name__)

app.secret_key="3c2c6be4-f63c-428a-9cd5-e909ba3b0e2a"

try:
    connect(host="mongodb://localhost:27017/localLens")
    if connection.get_connection():
        print("Database Connected.")
    else:
        print("Database not connected.")
except Exception as e:
    print(f"Error:{str(e)}")

app.register_blueprint(authBp)
app.register_blueprint(roleBp)
app.register_blueprint(userBp)
app.register_blueprint(issueBp)
app.register_blueprint(locationBp)
app.register_blueprint(statusBp)
app.register_blueprint(notificationBp)

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

if __name__=="__main__":
    app.run(debug=True)