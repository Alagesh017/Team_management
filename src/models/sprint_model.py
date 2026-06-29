import datetime
from src import db

class Sprint(db.Model):
    __tablename__ = "sprints"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    sprint_name = db.Column(db.String(200), nullable=False)
    sprint_goal = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    
    status = db.Column(db.String(30), default='PLANNED') # PLANNED | ACTIVE | COMPLETED | CANCELLED
    is_active = db.Column(db.Boolean, default=True)
    sprint_status = db.Column(db.Integer, default=0) # 0: Not Started, 1: Active, 2: Completed
    
    created_by = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', backref='sprints')
    
    def __repr__(self):
        return f"<Sprint {self.sprint_name}>"
