import datetime
from src import db

class TaskComment(db.Model):
    __tablename__ = "task_comments"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    role_id = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    remark = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    task = db.relationship('Task', backref='comments')
    
    def __repr__(self):
        return f"<TaskComment task_id={self.task_id} role={self.role} role_id={self.role_id}>"
