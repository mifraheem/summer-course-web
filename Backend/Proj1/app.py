from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    name = "Muhammad Ifraheem"
    skills = [ "Python", "JavaScript", "Golang", "PhP", "Java"]
    return render_template("home.html", name = name, mySkills=skills)


@app.route("/about")
def about():
    # return "this is about page"
    return render_template("about.html")

@app.route("/contact")
def contact():
    return "this is contact page v2"







if __name__ == "__main__":
    app.run(debug=True)