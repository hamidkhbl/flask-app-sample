from app import app
from flask import render_template, request, redirect
import pandas as pd
import os
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

app.config["FILE_UPLOADS"] = "E:/Google Drive/git/flask-app-sample/data"
app.config["ALLOWED_IMAGE_EXTENTIONS"] = ["CSV"]
app.config["MAX_FILE_SIZE"] = 0.5 * 1024 * 1024

def allowed_file(file_name):
    if not "." in file_name:
        return False
    ext = file_name.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENTIONS"]:
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
            f = request.files["file"]
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