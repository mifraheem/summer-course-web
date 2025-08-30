from app import db

saves = db.Table(
    'saves',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('pin_id', db.Integer, db.ForeignKey('pin.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profile_pic = db.Column(db.String(250), default="default.png")
    bio = db.Column(db.String(300), default="")
    pins = db.relationship('Pin', backref='owner', lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"
