from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"
# --- Database Config ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pinclone.db'

# --- File Upload Config ---
UPLOAD_FOLDER = os.path.join(os.getcwd(), "static/uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# make sure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # later hash this
    profile_pic = db.Column(db.String(250), default="default.png")
    bio = db.Column(db.String(300), default="")
    pins = db.relationship('Pin', backref='owner', lazy=True)
    # savedPins = 

    def __repr__(self):
        return f"<User {self.name}>"


class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    savers = db.relationship('User', secondary='saves', backref='saved_pins')
    def __repr__(self):
        return f"<Pin {self.title}>"
# Association table for saved pins
saves = db.Table(
    'saves',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('pin_id', db.Integer, db.ForeignKey('pin.id'), primary_key=True)
)

# Now add the relationship in Pin (or User)
Pin.savers = db.relationship('User', secondary=saves, backref='saved_pins')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login to continue.", "warning")
            return redirect(url_for("handleLogin"))
        return f(*args, **kwargs)
    return decorated_function


# --- Routes ---
@app.route("/")
@login_required
def home():
    pins = Pin.query.all()
    return render_template("/pins/home.html", pins=pins)


@app.route("/register", methods=["GET", "POST"])
def handleRegistration():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for("handleLogin"))

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create new user
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("handleLogin"))

    return render_template("/auth/registration.html")


@app.route("/login", methods=["GET", "POST"])
def handleLogin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("handleLogin"))

    return render_template("/auth/login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_name", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("handleLogin"))


@app.route("/user/<id>")
@login_required
def userProfile(id):
    user = User.query.get(id)
    return render_template("/pins/profile.html", user=user)

@app.route("/user/<id>/update", methods=["POST"])
@login_required
def updateProfile(id):
    user = User.query.get_or_404(id)

    # Ensure only the logged-in user can update
    if user.id != session["user_id"]:
        flash("You are not allowed to edit this profile.", "danger")
        return redirect(url_for("userProfile", id=id))

    user.name = request.form.get("name")
    user.bio = request.form.get("bio")

    # Handle profile picture
    file = request.files.get("profile_pic")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        user.profile_pic = filename  

    db.session.commit()
    flash("Profile updated successfully!", "success")
    return redirect(url_for("userProfile", id=user.id))


# --- Upload Pin Route ---
@app.route("/upload-pin", methods=["GET", "POST"])
@login_required
def uploadPin():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("caption")
        file = request.files.get("image")

        if not title or not file:
            flash("Title and image are required.", "danger")
            return redirect(url_for("uploadPin"))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # save relative path for DB
            image_url = f"uploads/{filename}"

            # save pin in DB
            new_pin = Pin(
                title=title,
                description=description,
                image_url=image_url,
                user_id=session["user_id"],
            )
            db.session.add(new_pin)
            db.session.commit()

            flash("Pin uploaded successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid file type. Only images allowed.", "danger")
            return redirect(url_for("uploadPin"))

    return render_template("/pins/createPin.html")


@app.route("/pin/<int:pin_id>/save", methods=["POST"])
@login_required
def savePin(pin_id):
    pin = Pin.query.get_or_404(pin_id)
    user = User.query.get(session["user_id"])

    # Check if already saved → unsave
    if pin in user.saved_pins:
        user.saved_pins.remove(pin)
        db.session.commit()
        flash("Pin removed from your saved list.", "info")
    else:
        user.saved_pins.append(pin)
        db.session.commit()
        flash("Pin saved successfully!", "success")

    # Redirect back where request came from
    return redirect(request.referrer or url_for("home"))


@app.route("/users")
@login_required
def allUsers():
    users = User.query.all()
    return render_template("/pins/users.html", users=users)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
