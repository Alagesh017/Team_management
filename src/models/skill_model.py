from src import db

class Skill(db.Model):
    __tablename__ = "skills"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)
    
    def __repr__(self):
        return f"<Skill {self.name}>"
