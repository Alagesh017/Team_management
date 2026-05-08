import datetime
from src import db

class ProjectGroup(db.Model):
    __tablename__ = "project_groups"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    projects = db.relationship('Project', backref='group', lazy=True)
    
    def __repr__(self):
        return f"<ProjectGroup {self.name}>"
