from app import app
from flask import render_template
import pandas as pd

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