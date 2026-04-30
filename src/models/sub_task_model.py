import datetime
from src import db

class SubTask(db.Model):
    __tablename__ = "sub_tasks"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('task_statuses.id'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default='medium') # low | medium | high | critical
    start_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # assigned to
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # who assigned
    estimated_hours = db.Column(db.Numeric(6, 2), nullable=True)
    actual_hours = db.Column(db.Numeric(6, 2), nullable=True)
    remark = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    parent_task = db.relationship('Task', backref='sub_tasks')
    status = db.relationship('TaskStatus', backref='sub_tasks')
    assigned_user = db.relationship('User', foreign_keys=[user_id], backref='assigned_sub_tasks')
    assigner = db.relationship('User', foreign_keys=[assigned_by], backref='assigned_by_sub_tasks')
    
    def __repr__(self):
        return f"<SubTask {self.title}>"
