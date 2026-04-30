import datetime
from src import db

class TaskAttachment(db.Model):
    __tablename__ = "task_attachments"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=True) # in bytes
    remark = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    task = db.relationship('Task', backref='attachments')
    user = db.relationship('User', backref='attachments')
    
    def __repr__(self):
        return f"<TaskAttachment {self.file_name}>"
