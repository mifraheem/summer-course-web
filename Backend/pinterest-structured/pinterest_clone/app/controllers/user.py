from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from functools import wraps
from app import db
from app.models.user import User

user_bp = Blueprint("user", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login to continue.", "warning")
            return redirect(url_for("user.handleLogin"))
        return f(*args, **kwargs)
    return decorated_function


@user_bp.route("/register", methods=["GET", "POST"])
def handleRegistration():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for("user.handleLogin"))

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("user.handleLogin"))

    return render_template("/auth/registration.html")


@user_bp.route("/login", methods=["GET", "POST"])
def handleLogin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for("pin.home"))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("user.handleLogin"))

    return render_template("/auth/login.html")


@user_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_name", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("user.handleLogin"))


@user_bp.route("/user/<id>")
@login_required
def userProfile(id):
    user = User.query.get(id)
    return render_template("/pins/profile.html", user=user)


@user_bp.route("/user/<id>/update", methods=["POST"])
@login_required
def updateProfile(id):
    user = User.query.get_or_404(id)

    if user.id != session["user_id"]:
        flash("You are not allowed to edit this profile.", "danger")
        return redirect(url_for("user.userProfile", id=id))

    user.name = request.form.get("name")
    user.bio = request.form.get("bio")

    file = request.files.get("profile_pic")
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join("app/static/uploads", filename)
        file.save(filepath)
        user.profile_pic = filename  

    db.session.commit()
    flash("Profile updated successfully!", "success")
    return redirect(url_for("user.userProfile", id=user.id))


@user_bp.route("/users")
@login_required
def allUsers():
    users = User.query.all()
    return render_template("/pins/users.html", users=users)
