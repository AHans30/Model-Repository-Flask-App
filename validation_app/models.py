from validation_app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(ad_id):
    return User.query.get(int(ad_id))

class User(db.Model, UserMixin):
    ad_id = db.Column(db.String(12), primary_key = True)
    password = db.Column(db.String(60), nullable = False)
    scorecards = db.relationship('Scorecard', backref = 'validator', lazy = True)

    def __repr__(self):
        return f"User({self.ad_id})"

class Scorecard(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product = db.Column(db.String(60), nullable = False)
    type = db.Column(db.String(60), nullable = False)
    deployment_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    discrimatory_power = db.Column(db.String(12), nullable = False)
    psi = db.Column(db.String(12), nullable = False)
    final_rating = db.Column(db.String(12), nullable = False)
    validator_id = db.Column(db.Integer, db.ForeignKey('user.ad_id'), nullable = False)
    
    def __repr__(self):
        return f"Scorecard({self.id}, {self.product}, {self.type})"