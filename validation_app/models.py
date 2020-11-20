from sqlalchemy.orm import backref
from validation_app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(ad_id):
    return User.query.get(int(ad_id))

# class User(db.Model, UserMixin):
#     ad_id = db.Column(db.String(12), primary_key = True)
#     password = db.Column(db.String(60), nullable = False)
#     scorecards = db.relationship('Scorecard', backref = 'validator', lazy = True)

#     def __repr__(self):
#         return f"User({self.ad_id})"

class Scorecard(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(60), nullable = False)
    product = db.Column(db.String(60), nullable = False)
    owner = db.Column(db.String(60), nullable = False)
    bad_definition = db.Column(db.String(60), nullable = False)
    dev_period = db.Column(db.String(60), nullable = False)
    pdv_period = db.Column(db.String(60), nullable = False)
    dev_ks = db.Column(db.Float, nullable = False)
    pdv_ks = db.Column(db.Float, nullable = False)
    relative_ks_change = db.Column(db.Float, nullable = False)
    psi = db.Column(db.Float, nullable = False)
    ks_absolute_rating = db.Column(db.String(12), nullable = False)
    ks_relative_rating = db.Column(db.String(12), nullable = False)
    discriminatory_rating = db.Column(db.String(12), nullable = False)
    psi_rating = db.Column(db.String(12), nullable = False)
    final_rating = db.Column(db.String(12), nullable = False)
    final_rating_comments = db.Column(db.UnicodeText, nullable = True)
    pdv_date = db.Column(db.DateTime, nullable=False)
    attached_report = db.Column(db.LargeBinary, nullable = False)
    attachment_name = db.Column(db.String(30), nullable = False)
    report_owner = db.Column(db.String(30), nullable = False)
    #full_report = db.Column(db.LargeBinary, nullable = True)
    #validator_id = db.Column(db.Integer, db.ForeignKey('user.ad_id'), nullable = False)
    monitorings = db.relationship('Monitoring', backref = 'scorecard')
    
    def __repr__(self):
        return f"Scorecard({self.id}, {self.product}, {self.type})"

class Monitoring(db.Model):
    monitoring_id = db.Column(db.Integer, primary_key = True)
    scorecard_id =  db.Column(db.Integer, db.ForeignKey('scorecard.id'))
    monitoring_period = db.Column(db.String(20), nullable = False)
    current_period = db.Column(db.String(20), nullable = False)
    proxy_bad_definition = db.Column(db.String(12), nullable = True)
    monitoring_ks = db.Column(db.Float, nullable = False)
    psi = db.Column(db.Float, nullable = False)
    relative_ks_change = db.Column(db.Float, nullable = False)
    ks_relative_rating = db.Column(db.String(12), nullable = False)
    discriminatory_rating = db.Column(db.String(12), nullable = False)
    psi_rating = db.Column(db.String(12), nullable = False)
    final_rating = db.Column(db.String(12), nullable = False)
    final_rating_comments = db.Column(db.UnicodeText, nullable = True)
    attached_report = db.Column(db.LargeBinary, nullable = False)
    attachment_name = db.Column(db.String(30), nullable = False)
    monitoring_date = db.Column(db.DateTime, nullable=False)
    report_owner = db.Column(db.String(30), nullable = False)