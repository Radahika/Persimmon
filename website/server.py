from flask import Flask
from flask import render_template
from flask import request

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

@app.route("/filter_page")
def filter_page():
    return jsonify(result=5)

if __name__ == "__main__":
    app.run()
