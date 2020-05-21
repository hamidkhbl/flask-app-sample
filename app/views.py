from app import app
from flask import render_template, request, redirect, make_response, session, url_for
import pandas as pd
import os
import sys
sys.path.append('app/models')
from User import User
from werkzeug.utils import secure_filename

@app.route("/")
def index():
    return render_template("public/index.html")

@app.route("/about")
def about():
    return render_template("public/about.html")

@app.route("/jinja")
def jinja():

    my_name = "Hamid"

    age = 30

    langs = ["Python", "JavaScript","C#","Java"]

    friends ={
        "Abbas":32,
        "Hamid": 32,
        "Ali":30
    }

    class GitRemote:
        def __init__(self, name, description, url):
            self.name = name
            self.description = description
            self.url = url
        def pull(self):
            return f"Pulling repo {self.name}"

        def clone(self):
            return f"cloning repo {self.name}"

    my_remote = GitRemote(name="flask", description = "test", url= "someurl")

    def repeat(x, qty):
        return x * qty

    df = pd.read_csv("data/test.csv")

    colors = ("Red", "Green")
    return render_template("public/jinja.html",
        my_name = my_name,
        age = age, langs = langs,
        colors = colors, friends = friends,
        GitRemote = GitRemote, repeat = repeat,
        data = df.to_html(classes="table table-hover table-striped table-sm"))

def allowed_file(file_name):
    if not "." in file_name:
        return False
    ext = file_name.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_FILE_EXTENTIONS"]:
        return True
    else:
        return False

def allowed_file_size(filesize):
    if int(filesize) <= app.config['MAX_FILE_SIZE']:
        return True
    else:
        return False

@app.route("/upload-file", methods=["POST", "GET"])
def upload_file():

    if request.method == "POST":
        if request.files:
            if not allowed_file_size(request.cookies.get("filesize")):
                print("File exceeded max file size")
                return redirect(request.url)

            print(request.cookies)
            f = request.files["csv"]
            if f.filename == "":
                print("File must have a file name.")
                return redirect(request.url)

            if not allowed_file(f.filename):
                print("file extention not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config["FILE_UPLOADS"], filename))
                print("Image saved")

            return redirect(request.url)

    return render_template("/public/upload-file.html")


@app.route("/sign-up", methods = ["POST", "GET"])
def sign_up():

    if request.method == "POST":
        req = request.form

        username = req.get("username")
        email = req.get("email")
        password = req.get("password")
        print(username, email, password)

        return redirect(request.url)

    return render_template("public/sign_up.html")

@app.route("/add-personal-info", methods = ["GET", "POST"])
def add_personal_info():

    if request.method == "POST":
        req = request.form
        user = User(name = req.get("name"),
            last_name = req.get("lastname"),
            email = req.get("email"),
            phone_number = req.get("phone_number"),
            age = req.get("age"),
            )
        user.add()
    return render_template("public/add_personal_info.html")


users = {
    "hamid": {
        "username":"hamid",
        "email":"hamid@yahoo.com",
        "password":"test",
        "bio":"hamid's bio"

    },
    "maryam": {
        "username":"maryam",
        "email":",maryam@yahoo.com",
        "password":"test",
        "bio":"maryam's bio"

    }
}

@app.route("/login", methods = ["GET", "POST"])
def login():
    print(request.method)

    if request.method == "POST":

        req = request.form
        username = req.get("username")
        password = req.get("password")

        if not username in users:
            print("username not found")
            return redirect(request.url)
        else:
            user = users[username]

        if not password in user["password"]:
            print("password incorrect")
            return redirect(request.url)
        else:
            session["USERNAME"] = user["username"]
            print("user added to session")
            return redirect(url_for("profile"))

    return render_template("public/login.html")

@app.route("/profile", methods = ["GET", "POST"])
def profile():

    if session.get("USERNAME", None) is not None:
        username = session.get('USERNAME')
        user = users[username]

        return render_template("public/profile.html", user = user)
    else:
        print("Username not found")
        return redirect(url_for("login"))


@app.route("/sign-out")
def sign_out():
    session.pop("USERNAME", None)
    return redirect(url_for("login"))