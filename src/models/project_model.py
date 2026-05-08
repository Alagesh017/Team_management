import datetime
from src import db

class Project(db.Model):
    __tablename__ = "projects"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('project_groups.id'), nullable=True)

    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), default='active') # active | on_hold | completed | cancelled
    project_logo = db.Column(db.String(500), nullable=True)
    remark = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    client = db.relationship('Client', backref='projects')
    creator = db.relationship('User', backref='created_projects')
    
    def __repr__(self):
        return f"<Project {self.name}>"
