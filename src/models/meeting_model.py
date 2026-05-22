import datetime
from src import db

class Meeting(db.Model):
    __tablename__ = "meetings"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    allocation_id = db.Column(db.Integer, db.ForeignKey('project_allocations.id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    
    title = db.Column(db.String(300), nullable=False)
    members = db.Column(db.JSON, nullable=False) # JSON array: [{role_id, role}]
    requirements = db.Column(db.Text, nullable=True)
    meeting_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=True)
    status = db.Column(db.String(30), default='scheduled') # scheduled | ongoing | completed | cancelled
    remark = db.Column(db.Text, nullable=True)
    created_by_role_id = db.Column(db.Integer, nullable=False)
    created_by_role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', backref='meetings')
    allocation = db.relationship('ProjectAllocation', backref='meetings')
    client = db.relationship('Client', backref='meetings')
    
    def __repr__(self):
        return f"<Meeting {self.title} created by {self.created_by_role} {self.created_by_role_id}>"
