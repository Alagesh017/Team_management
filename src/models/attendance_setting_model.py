import datetime 
from src import db 
 
class AttendanceSetting(db.Model): 
    __tablename__ = "attendance_settings" 
 
    attendance_setting_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
 
    # Working Week 
    week_start_day = db.Column(db.String(20), nullable=False)   # Monday 
    week_end_day = db.Column(db.String(20), nullable=False)     # Saturday 
 
    # Office Timing 
    start_time = db.Column(db.Time, nullable=False)             # 09:00 AM 
    end_time = db.Column(db.Time, nullable=False)               # 06:00 PM 
 
    # Expected Daily Working Hours 
    daily_working_hours = db.Column(db.Float, nullable=False)   # 8.0 
 
    is_active = db.Column(db.Boolean, default=True) 
 
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow) 
    updated_at = db.Column( 
        db.DateTime, 
        default=datetime.datetime.utcnow, 
        onupdate=datetime.datetime.utcnow 
    ) 
 
    def __repr__(self): 
        return f"<AttendanceSetting {self.week_start_day}-{self.week_end_day}>"