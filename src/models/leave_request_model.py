import datetime
from src import db

class LeaveRequest(db.Model):
    __tablename__ = "leave_requests"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False) # leave | permission
    reason = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=True) # for permission or half-day only
    end_time = db.Column(db.Time, nullable=True) # for permission or half-day only
    status = db.Column(db.String(20), default='pending') # pending | approved | rejected
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # admin or superadmin
    reviewed_at = db.Column(db.DateTime, nullable=True)
    review_comment = db.Column(db.Text, nullable=True)
    remark = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='leave_requests')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by], backref='reviewed_leaves')
    
    def __repr__(self):
        return f"<LeaveRequest {self.id} for User {self.user_id} - {self.status}>"
