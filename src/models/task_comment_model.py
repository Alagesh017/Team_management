import datetime
from src import db

class TaskComment(db.Model):
    __tablename__ = "task_comments"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    remark = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    task = db.relationship('Task', backref='comments')
    user = db.relationship('User', backref='task_comments')
    
    def __repr__(self):
        return f"<TaskComment task_id={self.task_id} user_id={self.user_id}>"
