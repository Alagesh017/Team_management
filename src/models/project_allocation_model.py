import datetime
from src import db

class ProjectAllocation(db.Model):
    __tablename__ = "project_allocations"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    members = db.Column(db.JSON, nullable=False, default=list) # JSON array: [{role_id, role}]
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    remark = db.Column(db.Text, nullable=True)
    allocated_by_role_id = db.Column(db.Integer, nullable=True)
    allocated_by_role = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', backref='allocations')
    
    def __repr__(self):
        return f"<ProjectAllocation project_id={self.project_id}>"
