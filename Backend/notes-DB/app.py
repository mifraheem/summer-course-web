from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.sqlite"
app.config["UPLOAD_FOLDER"] = "./uploads"
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(200), nullable=True)


@app.route('/')
def notes():
    allNotes = Note.query.all()
    return render_template("index.html", allNotes=allNotes)


@app.route("/create-note", methods=['GET', 'POST'])
def addNote():
    if request.method == 'POST':
        print("hey, user just posted a form...!")
        titleName = request.form["title"]
        contentData = request.form["content"]
        thumbnail = request.files['thumbnail']
        img_addr = None
        if thumbnail:
            newFileName = secure_filename(thumbnail.filename)
            
            thumbnail.save(os.path.join(app.config['UPLOAD_FOLDER'], newFileName))
            #save to db now
            print(newFileName)
            img_addr = newFileName

        new_note = Note(title=titleName, content=contentData, image_path=img_addr)
        db.session.add(new_note)
        db.session.commit()

    return render_template("add.html")

@app.route("/delete/<id>")
def deleteNote(id):
    note = Note.query.get(id)
    if note:
        db.session.delete(note)
        db.session.commit()
    return redirect("/")

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
