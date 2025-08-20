from flask import Flask, render_template, request, redirect, flash
import uuid

app = Flask(__name__)
app.secret_key = "slkdfsdlfkdsl"
NOTES = []

@app.route("/")
def homePage():
  allNotes = NOTES
  return render_template("home.html", allNotes=allNotes)

@app.route("/create-note", methods=["GET", "POST"])
def createNote():
  if request.method == 'POST':
    print(request.form)
    title = request.form['title']
    content = request.form['content']
    newNote = {
      'title': title,
      'content': content,
      'id': uuid.uuid4()
    }
    NOTES.append(newNote)
    flash("Note Created Successfully!")
    return redirect("/")
  return render_template("createNote.html")


@app.route("/delete-note/<id>")
def deleteNote(id):

  for ind, note in enumerate(NOTES):
    if str(note['id']) == str(id):
      NOTES.pop(ind)
  flash("Note has been deleted")
  return redirect('/')

if __name__ == "__main__":
  app.run(debug=True, port=5000)