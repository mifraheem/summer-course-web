from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# --- Database Config ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pinclone.db'


db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # later hash this
    profile_pic = db.Column(db.String(250), default="default.png")
    bio = db.Column(db.String(300), default="")
    pins = db.relationship('Pin', backref='owner', lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"


class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Pin {self.title}>"



# --- Routes ---
@app.route("/")
def home():
    return render_template("/pins/home.html")

@app.route("/register")
def handleRegistration():
    return render_template("/auth/registration.html")

@app.route("/login")
def handleLogin():
    return render_template("/auth/login.html")

@app.route("/user")
def userProfile():
    return render_template("/pins/profile.html")

@app.route("/upload-pin")
def uploadPin():
    return render_template("/pins/createPin.html")

@app.route("/users")
def allUsers():
    return render_template("/pins/users.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
