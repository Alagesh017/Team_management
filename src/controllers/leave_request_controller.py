from flask import jsonify, request
import datetime
from src import db
from src.models.leave_request_model import LeaveRequest

def create_leave_request(decoded_payload):
    try:
        data = request.get_json()
        
        user_id = decoded_payload.get("user_id")
        leave_type = data.get("type") # leave | permission
        reason = data.get("reason")
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")
        start_time_str = data.get("start_time")
        end_time_str = data.get("end_time")
        remark = data.get("remark")

        if not all([leave_type, reason, start_date_str, end_date_str]):
            return jsonify({"msg": "Type, Reason, Start Date, and End Date are required", "status": 0}), 400

        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
            start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time() if start_time_str else None
            end_time = datetime.datetime.strptime(end_time_str, '%H:%M').time() if end_time_str else None
        except ValueError:
            return jsonify({"msg": "Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time", "status": 0}), 400

        new_leave = LeaveRequest(
            user_id=user_id,
            type=leave_type,
            reason=reason,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time,
            remark=remark
        )
        db.session.add(new_leave)
        db.session.commit()
        
        return jsonify({"msg": "Leave request submitted successfully", "status": 1, "leave_id": new_leave.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def get_all_leave_requests():
    try:
        leaves = LeaveRequest.query.all()
        result = []
        for leave in leaves:
            result.append({
                "id": leave.id,
                "user_id": leave.user_id,
                "user_email": leave.user.email if leave.user else None,
                "type": leave.type,
                "reason": leave.reason,
                "start_date": leave.start_date.isoformat() if leave.start_date else None,
                "end_date": leave.end_date.isoformat() if leave.end_date else None,
                "start_time": leave.start_time.strftime('%H:%M') if leave.start_time else None,
                "end_time": leave.end_time.strftime('%H:%M') if leave.end_time else None,
                "status": leave.status,
                "reviewed_by": leave.reviewed_by,
                "reviewer_email": leave.reviewer.email if leave.reviewer else None,
                "reviewed_at": leave.reviewed_at.isoformat() if leave.reviewed_at else None,
                "review_comment": leave.review_comment,
                "remark": leave.remark,
                "created_at": leave.created_at.isoformat() if leave.created_at else None
            })
        return jsonify({"leaves": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def get_my_leave_requests(decoded_payload):
    try:
        user_id = decoded_payload.get("user_id")
        leaves = LeaveRequest.query.filter_by(user_id=user_id).all()
        result = []
        for leave in leaves:
            result.append({
                "id": leave.id,
                "type": leave.type,
                "reason": leave.reason,
                "start_date": leave.start_date.isoformat() if leave.start_date else None,
                "end_date": leave.end_date.isoformat() if leave.end_date else None,
                "status": leave.status,
                "review_comment": leave.review_comment,
                "created_at": leave.created_at.isoformat() if leave.created_at else None
            })
        return jsonify({"leaves": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def review_leave_request(leave_id, decoded_payload):
    try:
        leave = LeaveRequest.query.get(leave_id)
        if not leave:
            return jsonify({"message": "Leave request not found", "status": 0}), 404
        
        data = request.get_json()
        status = data.get("status") # approved | rejected
        review_comment = data.get("review_comment")
        
        if status not in ['approved', 'rejected']:
            return jsonify({"msg": "Status must be 'approved' or 'rejected'", "status": 0}), 400
            
        leave.status = status
        leave.review_comment = review_comment
        leave.reviewed_by = decoded_payload.get("user_id")
        leave.reviewed_at = datetime.datetime.utcnow()
        
        db.session.commit()
        return jsonify({"msg": f"Leave request {status} successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def delete_leave_request(leave_id, decoded_payload):
    try:
        leave = LeaveRequest.query.get(leave_id)
        if not leave:
            return jsonify({"message": "Leave request not found", "status": 0}), 404
        
        # Only the requester can delete their pending request
        if leave.user_id != decoded_payload.get("user_id"):
             return jsonify({"message": "Unauthorized to delete this request", "status": 0}), 403
        
        if leave.status != 'pending':
            return jsonify({"message": "Cannot delete a request that is already reviewed", "status": 0}), 400
            
        db.session.delete(leave)
        db.session.commit()
        return jsonify({"msg": "Leave request deleted successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500
