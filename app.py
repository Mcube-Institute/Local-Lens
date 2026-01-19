from flask import Flask,request,render_template,jsonify
from mongoengine import connect,connection
from models import *
from auth import authBp
from role import roleBp
from user import userBp
from issue import issueBp
from location import locationBp
from issueStatusHistory import statusBp

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

@app.get("/")
def home():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)