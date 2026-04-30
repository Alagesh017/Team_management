from src import db

class Education(db.Model):
    __tablename__ = "educations"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=True)
    specialization = db.Column(db.String(100), nullable=True)
    institution = db.Column(db.String(255), nullable=True)
    year_of_pass = db.Column(db.Integer, nullable=True)
    percentage = db.Column(db.Numeric(5, 2), nullable=True)
    
    def __repr__(self):
        return f"<Education {self.name}>"
