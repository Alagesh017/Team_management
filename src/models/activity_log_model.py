import datetime
from src import db

class ActivityLog(db.Model):
    __tablename__ = "activity_logs"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    table_name = db.Column(db.String(100), nullable=False) # users|admins|workers|clients|projects|...
    record_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(50), nullable=False) # created|updated|deleted|approved|rejected|...
    old_data = db.Column(db.Text, nullable=True) # JSON before
    new_data = db.Column(db.Text, nullable=True) # JSON after
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    remark = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<ActivityLog {self.id} - {self.role} {self.role_id} - {self.action} on {self.table_name}>"
