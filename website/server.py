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

    final_posts = []

    for post in posts:
        text = post.get("message", "")
        if len(text):
            summary = summarizer.summarize(text)
            post["summary"] = summary
            final_posts.append(post)

    return jsonify({"posts" : final_posts })


if __name__ == "__main__":
    app.run()
