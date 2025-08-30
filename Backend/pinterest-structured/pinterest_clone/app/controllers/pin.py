from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
from app import db
from app.models.pin import Pin
from app.models.user import User
from app.controllers.user import login_required

pin_bp = Blueprint("pin", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@pin_bp.route("/")
@login_required
def home():
    pins = Pin.query.all()
    return render_template("/pins/home.html", pins=pins)


@pin_bp.route("/upload-pin", methods=["GET", "POST"])
@login_required
def uploadPin():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("caption")
        file = request.files.get("image")

        if not title or not file:
            flash("Title and image are required.", "danger")
            return redirect(url_for("pin.uploadPin"))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join("app/static/uploads", filename)
            file.save(filepath)
            image_url = f"uploads/{filename}"

            new_pin = Pin(
                title=title,
                description=description,
                image_url=image_url,
                user_id=session["user_id"],
            )
            db.session.add(new_pin)
            db.session.commit()

            flash("Pin uploaded successfully!", "success")
            return redirect(url_for("pin.home"))
        else:
            flash("Invalid file type.", "danger")
            return redirect(url_for("pin.uploadPin"))

    return render_template("/pins/createPin.html")


@pin_bp.route("/pin/<int:pin_id>/save", methods=["POST"])
@login_required
def savePin(pin_id):
    pin = Pin.query.get_or_404(pin_id)
    user = User.query.get(session["user_id"])

    if pin in user.saved_pins:
        user.saved_pins.remove(pin)
        db.session.commit()
        flash("Pin removed from saved list.", "info")
    else:
        user.saved_pins.append(pin)
        db.session.commit()
        flash("Pin saved successfully!", "success")

    return redirect(request.referrer or url_for("pin.home"))


@pin_bp.route("/pin/<int:pin_id>/delete")
@login_required
def deletePin(pin_id):
    targetPin = Pin.query.get_or_404(pin_id)

    if targetPin.user_id != session.get("user_id"):
        flash("You are not allowed to delete this pin.", "danger")
        return redirect(url_for("pin.home"))

    db.session.delete(targetPin)
    db.session.commit()
    flash("Pin deleted successfully.", "success")
    return redirect(url_for("pin.home"))
