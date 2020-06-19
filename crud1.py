from flask import *
from PIL import Image
import sqlite3
import os
app = Flask(__name__)
#app.config.from_object(__name__)
app.config['UPLOAD_DIR'] = 'static/Uploads'

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/add")
def add():   
    return render_template("add.html")

@app.route("/savedetails",methods = ["POST","GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            gender = request.form["gender"]
            contact = request.form["contact"]
            dob = request.form["dob"]
            file = request.files["profile_pic"]
            #print(file)
            #print(request.form["name"])
            file.save(os.path.join(app.config['UPLOAD_DIR'],file.filename))
            with sqlite3.connect("users.db") as con:
                cur = con.cursor()   
                cur.execute("INSERT into users(name, email, gender, contact, dob, profile_pic) values (?,?,?,?,?,?)",(name,email,gender,contact,dob,file.filename))
                con.commit()
                msg = "User successfully Added"   
        except:
            con.rollback()
            msg = "We can not add User to the list"
        finally:
            return render_template("success.html",msg = msg)
            con.close()
if __name__ == "__main__":
    app.run(debug = True)  
