from flask import Flask, request, render_template, session, flash, url_for
from pymongo import MongoClient
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
import json

UPLOAD_FOLDER = r'C:\Users\abhinav\Downloads\updated_hms\hms\static\images\uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSION'] = ALLOWED_EXTENSIONS
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'abhinav.19203@gmail.com'
app.config['MAIL_PASSWORD'] = '9602770968'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
client = MongoClient()
db = client['customer']
collec = db['xyz'] 


@app.route("/")
def home():
    return render_template("login.html")

@app.route("/academics")
def academics():
    return render_template("academics.html")

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        father_name = request.form.get("father_name")
        dob = request.form.get("dob")
        email = request.form.get("email")
        mob = request.form.get("mob")
        course = request.form.get("course")
        year = request.form.get("year")
        user = request.form.get("user")
        branch = request.form.get("branch")
        hostel = request.form.get("hostel")


        if password == confirm:
            secure_password = str(password)
            entry = {'name': name,
                    'username': username,
                   'password': secure_password,
                    'father_name': father_name,
                     'dob': dob,
                     'email': email,
                     'mob': mob,
                     'course': course,
                     'year': year,
                     'branch': branch,
                     'file': "Avatar.svg",
                     'hostel': hostel,
                     'user': user,
                     }
            existing_user = collec.find_one({'username': username})
            session['username'] = username
            session['password'] = password
            session['name'] = name
            session['email'] = email
            session['father_name'] = father_name
            session['mob'] = mob
            session['dob'] = dob
            session['hostel'] = hostel
            if existing_user is None:
                collec.insert_one(entry)
                flash("Registration successful")
                return render_template("studentdashboard.html", filename="Avatar.svg", naming=name)
            else:
                flash("Username already exist")
                return render_template("register.html")
        else:
            flash("Password does not match")
            return render_template("register.html")
    else:
        return render_template("register.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        data = collec.find_one({"username": username, "password": password})
        if data:
            session['log'] = True
            flash("You are logged in")
            session['username'] = username
            session['password'] = password
            session['name'] = data['name']
            session['email'] = data['email']
            session['father_name'] = data['father_name']
            session['mob'] = data['mob']
            session['dob'] = data['dob']
            session['hostel'] = data['hostel']
            session['file'] = data['file']
            session['user'] = data['user']

            if data['user'] == "admin":
                return render_template("admindashboard.html", filename="Avatar.svg")
            if data['user'] == "Student":
                if data['file'] == "Avatar.svg" or data['file'] == "null":
                    return render_template("studentdashboard.html", naming=session['name'], filename="Avatar.svg")
                else:
                    return render_template("studentdashboard.html", naming=session['name'], filename=session['file'])
            else:
                return render_template("wardendashboard.html")
        else:
            flash("You are not registered")
            return render_template("register.html")
    else:
        return render_template("login.html")


@app.route("/wardenreg", methods=["GET", "POST"])
def wardenreg():
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        hostel = request.form.get("hostel")
        email = request.form.get("email")
        mob = request.form.get("mob")

        if password == confirm:
            secure_password = str(password)
            entry = {'name': name,
                     'username': username,
                     'password': secure_password,
                     'email': email,
                     'mob': mob,
                     'file': "Avatar.svg",
                     'hostel': hostel,
                     'father_name': "null", 'dob': "null", 'user': "warden"
                     }
            existing_user = collec.find_one({'username': username})
            if existing_user is None:
                collec.insert_one(entry)
                flash("Registration successful")

                return render_template("wardendashboard.html", filename="Avatar.svg")
            else:
                flash("Username already exist")
                return render_template("wardenregister.html", filename="Avatar.svg")
        else:
            flash("Password does not match")
            return render_template("wardenregister.html",filename="Avatar.svg")
    else:
        return render_template("wardenregister.html", filename="Avatar.svg")

@app.route("/hostel")
def hostel():
    return render_template("hostel.html", filename="Avatar.svg")

@app.route("/dashboard")
def dashboard():
    data = collec.find_one({"username": session['username']})
    if data['user'] == "warden":
        return render_template("wardendashboard.html")
    else:
        if data['file'] == "Avatar.svg":
            return render_template("studentdashboard.html", naming=session['name'], filename="Avatar.svg")
        else:
            return render_template("studentdashboard.html", naming=session['name'], filename=data['file'])

@app.route("/logout")
def logout():
    session.clear()
    flash("You are now logged out")
    return render_template("login.html")

@app.route("/query" ,methods=["POST","GET"])
def query():
    if request.method == "POST":
        name = request.form.get("name")
        data = collec.find({"name": name}, {"_id": 0, "password": 0, "user": 0, "name": 0, "file": 0})
        if data:
            return render_template("studentquery.html", datas=list(data))
        else:
            flash("Record Not found")
            return render_template("studentquery.html", datas={})
    else:
        return render_template("studentquery.html", datas={})

@app.route("/query1" ,methods=["POST","GET"])
def query1():
    if request.method == "POST":
        name = request.form.get("name")
        data = collec.find({"name": name}, {"_id": 0, "password": 0, "user": 0, "name": 0, "file": 0})
        if data:
            return render_template("studentquery1.html", datas=list(data))
        else:
            flash("Record Not found")
            return render_template("studentquery1.html", datas={})
    else:
        return render_template("studentquery1.html", datas={})

@app.route("/queryall1")
def queryall1():
   if session['hostel'] == "Aryabhatta Hostel":
       data = collec.find({"hostel": "Aryabhatta"},{"_id": 0, "password": 0, "user": 0, "username": 0, "file": 0, "father_name": 0, "dob": 0,"email": 0, "complain": 0, "hostel": 0})
       c = collec.count({"hostel": "Aryabhatta"})
       return render_template("hostel_info1.html", datas=list(data), count=c, hos="Aryabhatta Hostel",filename=session['file'])
   else:
       data = collec.find({"hostel": "Vikram Sarabhai"},{"_id": 0, "password": 0, "user": 0, "username": 0, "file": 0, "father_name": 0, "dob": 0,"email": 0, "complain": 0, "hostel": 0})
       c = collec.count({"hostel": "Vikram Sarabhai"})
       return render_template("hostel_info1.html", datas=list(data), count=c, hos="Vikram Sarabhai Hostel",filename=session['file'])


@app.route("/queryall")
def queryall():
    return render_template("hostel.html", filename=session['file'])

@app.route("/hostel_info1")
def hostel_info1():
    data = collec.find({"hostel":"Aryabhatta"},{"_id": 0,"password": 0,"user": 0,"username":0,"file": 0,"father_name":0,"dob":0,"email":0,"complain":0,"hostel":0})
    c = collec.count({"hostel":"Aryabhatta"})
    return render_template("hostel_info.html",datas=list(data),count=c,hos="Aryabhatta Hostel",filename=session['file'])

@app.route("/hostel_info2")
def hostel_info2():
    data = collec.find({"hostel":"Vikram Sarabhai"},{"_id": 0,"password": 0,"user": 0,"username":0,"file": 0,"father_name":0,"dob":0,"email":0,"complain":0,"hostel":0})
    c = collec.count({"hostel": "Vikram Sarabhai"})
    return render_template("hostel_info.html",datas=list(data),count=c,hos="Vikram Sarabhai Hostel",filename=session['file'])

@app.route("/allotment", methods=["POST","GET"])
def allotment():
    if request.method == "POST":
        room = request.form.get("room")
        prev = collec.find_one({"room": room})
        if prev is None:
            collec.update_one({"username": session['username']}, {"$set": {"room": room}})
            msg = Message('Room allotment', sender='abhinav.19203@gmail.com', recipients=[session['email']])
            msg.body = "Room No. {} alloted".format(room)
            mail.send(msg)
            flash("Room No. {} alloted and mail send".format(room))
            return render_template("academics.html")
        else:
            flash("Room is already alloted")
            return render_template("roomallotment_1.html")
    else:
        if session['hostel'] == "Aryabhatta":
            return render_template("roomallotment_2.html")
        else:
            return render_template("roomallotment_1.html")

@app.route("/update",methods=["POST","GET"])
def update():
    if request.method == "POST":
        username = request.form.get("username")
        existing_username = collec.find_one({"username": username})
        if existing_username is None:
            collec.update_one({"username": session['username']}, {"$set": {"username": username}})
            flash("Update Successful")
            return render_template("update.html", name=session['name'], username=username,
                                   mob=session['mob'], email=session['email'], password=session['password'],
                                   father_name=session['father_name'], dob=session['dob'],filename=session['file'],naming=session['name'])
        else:
            flash("Username already exist")
            return render_template("update.html", name=session['name'], username=session['username'],
                                   mob=session['mob'], email=session['email'], password=session['password'],
                                   father_name=session['father_name'], dob=session['dob'],filename=session['file'],naming=session['name'])
    else:
        return render_template("update.html", name=session['name'], username=session['username'], mob=session['mob'], email=session['email'], password=session['password'],father_name=session['father_name'],dob=session['dob'],filename=session['file'],naming=session['name'])

def allowed_file(filename):
    if not '.' in filename:
        return False
    ext = filename.rsplit('.', 1)[1]
    if ext.lower() in app.config["ALLOWED_EXTENSION"]:
        return True
    else:
        return False

@app.route("/complain",methods=["GET","POST"])
def complain():
    if request.method == "POST":
        complain = request.form.get("comp")
        collec.update_one({"name": session['name']}, {"$set": {"complain": complain}})
        flash("Complain registered")
        return render_template("complain.html", filename=session['file'], naming=session['name'])
    else:
        return render_template("complain.html", filename=session['file'], naming=session['name'])

@app.route("/complain_to")
def complain_to():
    if session['hostel'] == "Aryabhatta hostel":
        data = collec.find({"hostel": "Aryabhatta"},{"_id":0,"password":0,"user":0,"file":0,"username":0,"father_name":0,"dob":0,"year":0,"branch":0,"course":0,"hostel":0,"email":0,"mob":0})
        return render_template("complain1.html", datas=list(data))
    else:
        data = collec.find({"hostel": "Vikram Sarabhai"},{"_id":0,"password":0,"user":0,"file":0,"username":0,"father_name":0,"dob":0,"year":0,"branch":0,"course":0,"hostel":0,"email":0,"mob":0})
        return render_template("complain1.html", datas=list(data))

@app.route("/upload",methods=["GET","POST"])
def upload_file():
    if request.method == 'POST':
        if request.files:
            file = request.files['file']
            if file.filename == '':
                flash("No file selected")
                return render_template("upload.html", filename="Avatar.svg")
            if not allowed_file(file.filename):
                flash("File extension not allowed")
                return render_template("upload.html", filename="Avatar.svg")
            else:
                filename = secure_filename(file.filename)
                session['file'] = filename
                existing_file = collec.find_one({"file": session['file']})
                if existing_file is None:
                    collec.update_one({"username": session['username']}, {"$set": {"file": session['file']}})
                else:
                    flash("File name already exist")
                    return render_template("upload.html", filename="Avatar.svg",naming=session['name'])

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash("Profile successfully uploaded")
                return render_template("upload.html", filename=filename, naming=session['name'])
    else:
        return render_template("upload.html", filename=session['file'], naming=session['name'])


app.secret_key = "12ddededd"
app.run(debug=True)
