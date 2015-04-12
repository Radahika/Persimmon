from flask import Flask
from flask import render_template
from flask import request

import os
import pdb

from summarizer import summarizer

app = Flask(__name__)
app.debug = True

#pagination
POSTS_PER_PAGE = 20

@app.route("/")
def login():
    return render_template("index.html")

@app.route("/home")
@app.route("/home/page/<int:page>")
def home(page=1):
    feed = [["Kevin Hwang", "Radhika is cool"], ["Radhika Marvin", "Kevin is cute"]]
    return render_template("home.html", feed=feed)

@app.route("/summary", methods=["POST"])
def summary():
    text = request.form.get("text")
    summary = summarizer.summarize(text)
    return summary


if __name__ == "__main__":
    app.run()
