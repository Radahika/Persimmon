from flask import Flask
from flask import render_template
from flask import request, jsonify

import json
import os
import pdb

from summarizer import summarizer
from sentiment import train

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

#@app.route("/filter_page")
#def filter_page(label="happy"):
    #feed = [{"author": "Kevin Hwang", "text": "Radhika Marvin is hott!"},
                #{"author": "Radhika Marvin", "text": "Kevin has a cute butt!!!"},
                #{"author": "Dizzy Tarakci", "text": "I hate my sad life. O-chem sucks"}
              #]
    #trainer = train.Trainer() #Automatically run trainer on sampled data
    #result = {}
    #result["posts"] = []
    #for post in feed:
        #score = trainer.guess(post["text"])
        #print score
        #if score[label] >= 0.75:
            #summary = summarizer.summarize(post["text"])
            #post["summary"] = summary
            #result["posts"].append(post)
    #return jsonify(result)

@app.route("/filter_page", methods=["POST"])
def filter_page():
    post_string = request.form.get("posts")

    posts = json.loads(post_string)

    final_posts = []

    for post in posts:
        text = post.get("message", "")
        if len(text):
            summary = summarizer.summarize(text)
            final_post = {}
            final_post["author"] = post.get("from").get("name")
            final_post["text"] = post.get("message")
            final_post["summary"] = summary
            final_posts.append(final_post)

    return jsonify({"posts" : final_posts })


if __name__ == "__main__":
    app.run()
