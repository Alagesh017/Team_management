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
    role_id = db.Column(db.Integer, nullable=True) # admin.id or worker.id
    role = db.Column(db.String(50), nullable=True) # admin or worker
    assigned_by_role_id = db.Column(db.Integer, nullable=False) # who assigned (role_id)
    assigned_by_role = db.Column(db.String(50), nullable=False) # who assigned (role)
    estimated_hours = db.Column(db.Numeric(6, 2), nullable=True)
    actual_hours = db.Column(db.Numeric(6, 2), nullable=True)
    remark = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    parent_task = db.relationship('Task', backref='sub_tasks')
    status = db.relationship('TaskStatus', backref='sub_tasks')
    
    def __repr__(self):
        return f"<SubTask {self.title}>"
