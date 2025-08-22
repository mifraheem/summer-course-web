from flask import Flask , render_template, request
import os

UPLOAD_FOLDER = "./uploads"

app=Flask (__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/add", methods=['GET', 'POST'])
def add():
  if request.method == 'POST':
  
     file = request.files['profilePicture']

     
     file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

  return render_template("add.html")


if __name__ == "__main__":
  app.run(debug=True, port=5000)