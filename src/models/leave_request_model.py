import datetime
from src import db

class LeaveRequest(db.Model):
    __tablename__ = "leave_requests"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(20), nullable=False) # leave | permission
    reason = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=True) # for permission or half-day only
    end_time = db.Column(db.Time, nullable=True) # for permission or half-day only
    status = db.Column(db.String(20), default='pending') # pending | approved | rejected
    reviewed_by_role_id = db.Column(db.Integer, nullable=True) # admin or superadmin
    reviewed_by_role = db.Column(db.String(50), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    review_comment = db.Column(db.Text, nullable=True)
    remark = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<LeaveRequest {self.id} for {self.role} {self.role_id} - {self.status}>"
