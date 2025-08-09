from flask import Flask, render_template
server = Flask(__name__)
@server.route("/api/students")
def stdData():
  students = ["Sudais", "Mehnaz", "Arina"]
  return students


@server.route("/students")
def stdDataForWeb():
  students = ["Sudais khan", "Mehnaz Ali", "Arina Itfaq"]
  return render_template("data.html", data=students)


@server.route("/")
def home():
  pass


@server.route("/about")
def about():
  pass

@server.route("/services")
def services():
  pass