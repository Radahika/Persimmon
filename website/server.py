from flask import Flask
from flask import render_template

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

if __name__ == "__main__":
    app.run()
