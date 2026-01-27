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
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")


@app.get("/logout")
def logout():
    session.clear()
    return redirect("/login")

DEV_ISSUE_BYPASS = True

@app.before_request
def temp_issue_creation_session():
    if DEV_ISSUE_BYPASS and request.path == "/issue/new" and "user" not in session:
        session["user"] = {
            "id": "5c800c6b-7297-4366-b308-984f4af3870d",
            "name": "SomeOne",
            "email": "some@one.com"
        }

if __name__=="__main__":
    app.run(debug=True)