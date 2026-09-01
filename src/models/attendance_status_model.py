import datetime
from src import db

class AttendanceStatus(db.Model):
    __tablename__ = "attendance_statuses"
    
    attendance_status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_name = db.Column(db.String(50), nullable=False, unique=True)
    status_code = db.Column(db.String(10), nullable=False, unique=True)
    is_present = db.Column(db.Boolean, default=False)
    is_absent = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<AttendanceStatus {self.status_name}>"
