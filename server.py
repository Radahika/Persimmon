from flask import Flask
from flask import render_template
from flask import request, jsonify

import json
import os
import pdb

from summarizer import summarizer
from sentiment import train
from sentiment import example

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

@app.route("/summarizer_page", methods=["GET"])
def summarizer_page():
    return render_template("summarizer.html");

@app.route("/filter_page", methods=["POST"])
def filter_page(label="happy"):
    post_string = request.form.get("posts")
    posts = json.loads(post_string)

    trainer = train.Trainer()

    final_posts = []

    for post in posts:
        text = post.get("message")

        if not text:
            text = post.get("caption")
        if not text:
            text = post.get("story")

        if text:
            score = trainer.guess(text)
            if score[label] >= 0.75:
                final_post = {}
                summary = summarizer.summarize(text)
                final_post["author"] = post.get("from").get("name")
                final_post["text"] = text
                final_post["summary"] = summary
                final_posts.append(final_post)
    return jsonify({"posts" : final_posts })

@app.route('/training')
def training():
    trainer = train.Trainer()
    #print trainer.arg_max("I am just so so so happy!!!")
    #print trainer.arg_max("Fuck life. I'm so done with this shit. Ugh.")
    return render_template("home.html")



if __name__ == "__main__":
    app.run()
