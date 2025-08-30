from app import db
from datetime import datetime
from app.models.user import saves

class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    savers = db.relationship('User', secondary=saves, backref='saved_pins')

    def __repr__(self):
        return f"<Pin {self.title}>"
