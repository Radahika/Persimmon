from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import json
import os
import pdb

from summarizer import summarizer

app = Flask(__name__)
app.debug = True

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/summary", methods=["POST"])
def summary():
    text = request.form.get("text")
    summary = summarizer.summarize(text)
    return summary

@app.route("/filter_page", methods=["POST"])
def filter_page():
    post_string = request.form.get("posts")

    posts = json.loads(post_string)

    return jsonify({"posts" : posts })


if __name__ == "__main__":
    app.run()
