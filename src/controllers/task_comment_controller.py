from flask import jsonify, request
import datetime
from src import db
from src.models.task_comment_model import TaskComment

def create_comment(decoded_payload):
    try:
        data = request.get_json()
        
        task_id = data.get("task_id")
        comment = data.get("comment")
        remark = data.get("remark")
        
        user_id = decoded_payload.get("user_id")

        if not task_id or not comment:
            return jsonify({"msg": "Task ID and comment are required", "status": 0}), 400

        new_comment = TaskComment(
            task_id=task_id,
            user_id=user_id,
            comment=comment,
            remark=remark
        )
        db.session.add(new_comment)
        db.session.commit()
        
        return jsonify({"msg": "Comment added successfully", "status": 1, "id": new_comment.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def get_comments_by_task(task_id):
    try:
        comments = TaskComment.query.filter_by(task_id=task_id).order_by(TaskComment.created_at.desc()).all()
        result = []
        for c in comments:
            result.append({
                "id": c.id,
                "task_id": c.task_id,
                "user_id": c.user_id,
                "user_email": c.user.email if c.user else None,
                "comment": c.comment,
                "remark": c.remark,
                "created_at": c.created_at
            })
        return jsonify({"comments": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def get_comment_by_id(comment_id):
    try:
        c = TaskComment.query.get(comment_id)
        if not c:
            return jsonify({"message": "Comment not found", "status": 0}), 404
        
        result = {
            "id": c.id,
            "task_id": c.task_id,
            "user_id": c.user_id,
            "user_email": c.user.email if c.user else None,
            "comment": c.comment,
            "remark": c.remark,
            "created_at": c.created_at
        }
        return jsonify({"comment": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def update_comment(comment_id, decoded_payload):
    try:
        c = TaskComment.query.get(comment_id)
        if not c:
            return jsonify({"message": "Comment not found", "status": 0}), 404

        # Only allow the author to update their comment
        if c.user_id != decoded_payload.get("user_id"):
            return jsonify({"message": "Unauthorized to update this comment", "status": 0}), 403

        data = request.get_json()
        
        if "comment" in data:
            c.comment = data["comment"]
        if "remark" in data:
            c.remark = data["remark"]
            
        db.session.commit()
        return jsonify({"message": "Comment updated successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def delete_comment(comment_id, decoded_payload):
    try:
        c = TaskComment.query.get(comment_id)
        if not c:
            return jsonify({"message": "Comment not found", "status": 0}), 404
            
        # Only allow the author to delete their comment
        if c.user_id != decoded_payload.get("user_id"):
            return jsonify({"message": "Unauthorized to delete this comment", "status": 0}), 403

        db.session.delete(c)
        db.session.commit()
        return jsonify({"message": "Comment deleted successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500
