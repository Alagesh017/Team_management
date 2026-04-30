import datetime
from src import db

class ProjectAllocation(db.Model):
    __tablename__ = "project_allocations"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    members = db.Column(db.JSON, nullable=False) # JSON array: [{user_id, role}]
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    remark = db.Column(db.Text, nullable=True)
    allocated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', backref='allocations')
    allocator = db.relationship('User', backref='project_allocations')
    
    def __repr__(self):
        return f"<ProjectAllocation project_id={self.project_id}>"
