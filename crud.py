from flask import *
from PIL import Image
from datetime import date 
import sqlite3
import os
app = Flask(__name__)
#app.config.from_object(__name__)
app.config['UPLOAD_DIR'] = 'static/Uploads'

def get_post(id):
    con = sqlite3.connect("users.db")
    con.row_factory = sqlite3.Row
    user = con.execute('SELECT * FROM users WHERE id = ?',
                        (id,)).fetchone()
    con.close()
    if user is None:
        abort(404)
    return user

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

@app.route("/view")
def view():
    con = sqlite3.connect("users.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from users")   
    rows = cur.fetchall()
    current_date =  date.today()
    return render_template("view.html",rows = rows, now_date = current_date)

@app.route("/<int:id>/view_user", methods=("GET", "POST"))
def view_user(id):
    row = get_post(id)
    current_date = date.today()
    return render_template("view_user.html",row = row, now_date = current_date)

@app.route("/<int:id>/edit_user", methods=("GET", "POST"))
def edit_user(id):
    user = get_post(id)

    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        gender = request.form["gender"]
        contact = request.form["contact"]
        dob = request.form["dob"]
        file = request.files["profile_pic"]
        file.save(os.path.join(app.config['UPLOAD_DIR'],file.filename))
        with sqlite3.connect("users.db") as con:
            cur = con.cursor()   
            cur.execute("Update users set name = ?, email = ?, gender = ?, contact = ?, dob = ?, profile_pic = ?",(name,email,gender,contact,dob,file.filename))
            con.commit()
            return redirect(url_for('index'))
    return render_template('edit_user.html', user = user)
    

if __name__ == "__main__":
    app.run(debug = True)  
