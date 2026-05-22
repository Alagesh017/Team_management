import datetime
from src import db

class MeetingMessage(db.Model):
    __tablename__ = "meeting_messages"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    role_id = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True) # null if only attachment sent
    attachment_url = db.Column(db.String(500), nullable=True)
    attachment_name = db.Column(db.String(255), nullable=True)
    is_edited = db.Column(db.Boolean, default=False)
    edited_at = db.Column(db.DateTime, nullable=True)
    remark = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    meeting = db.relationship('Meeting', backref='messages')
    
    def __repr__(self):
        return f"<MeetingMessage {self.id} by {self.role} {self.role_id}>"
