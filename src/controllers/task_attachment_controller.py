from flask import jsonify, request
import datetime
from src import db
from src.models.task_attachment_model import TaskAttachment

def create_attachment(decoded_payload):
    try:
        data = request.get_json()
        
        task_id = data.get("task_id")
        file_name = data.get("file_name")
        file_url = data.get("file_url")
        file_size = data.get("file_size")
        remark = data.get("remark")
        
        user_id = decoded_payload.get("user_id")

        if not all([task_id, file_name, file_url]):
            return jsonify({"msg": "Task ID, File Name, and File URL are required", "status": 0}), 400

        new_attachment = TaskAttachment(
            task_id=task_id,
            user_id=user_id,
            file_name=file_name,
            file_url=file_url,
            file_size=file_size,
            remark=remark
        )
        db.session.add(new_attachment)
        db.session.commit()
        
        return jsonify({"msg": "Attachment created successfully", "status": 1, "attachment_id": new_attachment.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def get_all_attachments():
    try:
        attachments = TaskAttachment.query.all()
        result = []
        for attachment in attachments:
            result.append({
                "id": attachment.id,
                "task_id": attachment.task_id,
                "task_title": attachment.task.title if attachment.task else None,
                "user_id": attachment.user_id,
                "user_email": attachment.user.email if attachment.user else None,
                "file_name": attachment.file_name,
                "file_url": attachment.file_url,
                "file_size": attachment.file_size,
                "remark": attachment.remark,
                "created_at": attachment.created_at.isoformat() if attachment.created_at else None,
                "updated_at": attachment.updated_at.isoformat() if attachment.updated_at else None
            })
        return jsonify({"attachments": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def get_attachment_by_id(attachment_id):
    try:
        attachment = TaskAttachment.query.get(attachment_id)
        if not attachment:
            return jsonify({"message": "Attachment not found", "status": 0}), 404
        
        result = {
            "id": attachment.id,
            "task_id": attachment.task_id,
            "task_title": attachment.task.title if attachment.task else None,
            "user_id": attachment.user_id,
            "user_email": attachment.user.email if attachment.user else None,
            "file_name": attachment.file_name,
            "file_url": attachment.file_url,
            "file_size": attachment.file_size,
            "remark": attachment.remark,
            "created_at": attachment.created_at.isoformat() if attachment.created_at else None,
            "updated_at": attachment.updated_at.isoformat() if attachment.updated_at else None
        }
        return jsonify({"attachment": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def update_attachment(attachment_id):
    try:
        attachment = TaskAttachment.query.get(attachment_id)
        if not attachment:
            return jsonify({"message": "Attachment not found", "status": 0}), 404
        
        data = request.get_json()
        
        attachment.file_name = data.get("file_name", attachment.file_name)
        attachment.file_url = data.get("file_url", attachment.file_url)
        attachment.file_size = data.get("file_size", attachment.file_size)
        attachment.remark = data.get("remark", attachment.remark)
        
        db.session.commit()
        return jsonify({"msg": "Attachment updated successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def delete_attachment(attachment_id):
    try:
        attachment = TaskAttachment.query.get(attachment_id)
        if not attachment:
            return jsonify({"message": "Attachment not found", "status": 0}), 404
        
        db.session.delete(attachment)
        db.session.commit()
        return jsonify({"msg": "Attachment deleted successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500
