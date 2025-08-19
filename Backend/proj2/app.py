from flask import Flask, render_template, request

app = Flask(__name__)
STUDENTS = ["asmara", "hira", "arina", "amna", "aliza"]

@app.route("/")
def home():
  return render_template("home.html")



@app.route("/students")
def students():
  
  return STUDENTS

@app.route("/students/<name>")
def checkStd(name):
  if name in STUDENTS:
    return f"Yes, {name} exists in database"
  else:
    return f"No, {name} doesn't exists in database"


@app.route("/students/graduated")
def grdStd():
  return "we haven't any student."


@app.route("/register", methods=['POST', 'GET'])
def register():
  print(f"The current request method is: {request.method}")

  if request.method == 'POST':
    email = request.form["email"]
    psd = request.form["password"]
    print(email, psd)
  return render_template("register.html")

if __name__ == "__main__":
  app.run(debug=True, port=8000)