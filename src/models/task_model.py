import datetime
from src import db

class Task(db.Model):
    __tablename__ = "tasks"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    allocation_id = db.Column(db.Integer, db.ForeignKey('project_allocations.id'), nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey('task_statuses.id'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=True)
    goal = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default='medium') # low | medium | high | critical
    start_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False) # assigned to (Worker ID)
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # who assigned (User ID)
    responsibility_person_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=True) # person responsible (Worker ID)
    estimated_hours = db.Column(db.Numeric(6, 2), nullable=True)
    actual_hours = db.Column(db.Numeric(6, 2), nullable=True)
    remark = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', backref='tasks')
    allocation = db.relationship('ProjectAllocation', backref='tasks')
    status = db.relationship('TaskStatus', backref='tasks')
    assigned_worker = db.relationship('Worker', foreign_keys=[worker_id], backref='assigned_tasks')
    assigner = db.relationship('User', foreign_keys=[assigned_by], backref='assigned_by_tasks')
    responsibility_person = db.relationship('Worker', foreign_keys=[responsibility_person_id], backref='responsible_tasks')
    
    def __repr__(self):
        return f"<Task {self.title}>"
