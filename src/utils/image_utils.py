import os
import uuid
import base64
from flask import current_app

def save_image(image_data, folder="profile_images"):
    try:
        if not image_data:
            return None
        
        # Check if it's already a saved path or an external URL
        if isinstance(image_data, str) and (image_data.startswith("/src/assets/") or image_data.startswith("/api/v1/src/assets/") or image_data.startswith("http")):
            return image_data
        
        # Check if it's a base64 string
        if isinstance(image_data, str) and image_data.startswith("data:image"):
            try:
                header, encoded = image_data.split(",", 1)
                file_ext = header.split("/")[1].split(";")[0]
                filename = f"{uuid.uuid4()}.{file_ext}"
                
                # Ensure the target directory exists
                base_path = current_app.config["SERVE_STATIC_FOLDER"]
                target_dir = os.path.join(base_path, folder)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)
                
                filepath = os.path.join(target_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(encoded))
                
                # Return the relative URL for frontend consumption
                return f"/src/assets/{folder}/{filename}"
            except Exception as inner_e:
                current_app.logger.error(f"Failed to decode/save base64 image: {inner_e}")
                return None
            
        return None
    except Exception as e:
        if current_app:
            current_app.logger.error(f"Error in save_image: {e}")
        return None

def delete_image(image_url):
    try:
        if not image_url:
            return True
        
        # Skip if it's an external URL (not our asset)
        if image_url.startswith("http") and not image_url.startswith("/src/assets/") and not image_url.startswith("/api/v1/src/assets/"):
            return True
        
        # Extract the file path from the URL
        if image_url.startswith("/api/v1/src/assets/"):
            relative_path = image_url.replace("/api/v1/src/assets/", "")
        elif image_url.startswith("/src/assets/"):
            relative_path = image_url.replace("/src/assets/", "")
        else:
            # Not our asset format, skip
            return True
        
        # Get the full file path
        base_path = current_app.config["SERVE_STATIC_FOLDER"]
        full_path = os.path.join(base_path, relative_path)
        
        # Delete the file if it exists
        if os.path.exists(full_path) and os.path.isfile(full_path):
            os.remove(full_path)
            return True
        
        return False
    except Exception as e:
        if current_app:
            current_app.logger.error(f"Error in delete_image: {e}")
        return False

def save_file(file_data, folder="project_excels", file_ext="xlsx"):
    try:
        if not file_data:
            return None
        
        # Check if it's already a saved path or an external URL
        if isinstance(file_data, str) and (file_data.startswith("/src/assets/") or file_data.startswith("/api/v1/src/assets/") or file_data.startswith("http")):
            return file_data
        
        # Check if it's a base64 string
        if isinstance(file_data, str) and file_data.startswith("data:"):
            try:
                # Extract the file extension if available, otherwise use the provided one
                if file_data.startswith("data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
                    file_ext = "xlsx"
                elif file_data.startswith("data:application/vnd.ms-excel"):
                    file_ext = "xls"
                else:
                    # Try to extract extension from mime type
                    header_part = file_data.split(",")[0]
                    if "/" in header_part:
                        mime_type = header_part.split(":")[1].split(";")[0]
                        ext_from_mime = mime_type.split("/")[-1]
                        if ext_from_mime:
                            file_ext = ext_from_mime
                
                header, encoded = file_data.split(",", 1)
                filename = f"{uuid.uuid4()}.{file_ext}"
                
                # Ensure the target directory exists
                base_path = current_app.config["SERVE_STATIC_FOLDER"]
                target_dir = os.path.join(base_path, folder)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)
                
                filepath = os.path.join(target_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(encoded))
                
                # Return the relative URL for frontend consumption
                return f"/src/assets/{folder}/{filename}"
            except Exception as inner_e:
                current_app.logger.error(f"Failed to decode/save base64 file: {inner_e}")
                return None
            
        return None
    except Exception as e:
        if current_app:
            current_app.logger.error(f"Error in save_file: {e}")
        return None

def save_attachment(file_data, file_name=None, folder="attachments"):
    try:
        if not file_data:
            return None
        
        # Check if it's already a saved path or an external URL
        if isinstance(file_data, str) and (file_data.startswith("/src/assets/") or file_data.startswith("/api/v1/src/assets/") or file_data.startswith("http")):
            return file_data
        
        # Check if it's a base64 string
        if isinstance(file_data, str) and file_data.startswith("data:"):
            try:
                # Extract file extension
                header, encoded = file_data.split(",", 1)
                mime_type = header.split(":")[1].split(";")[0]
                # Try to get extension from filename if provided, else from mime type
                if file_name:
                    file_ext = file_name.split(".")[-1]
                else:
                    file_ext = mime_type.split("/")[-1]
                
                filename = f"{uuid.uuid4()}.{file_ext}"
                
                # Ensure the target directory exists
                base_path = current_app.config["SERVE_STATIC_FOLDER"]
                target_dir = os.path.join(base_path, folder)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)
                
                filepath = os.path.join(target_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(encoded))
                
                # Return the relative URL for frontend consumption
                return f"/src/assets/{folder}/{filename}"
            except Exception as inner_e:
                current_app.logger.error(f"Failed to decode/save base64 attachment: {inner_e}")
                return None
            
        return None
    except Exception as e:
        if current_app:
            current_app.logger.error(f"Error in save_attachment: {e}")
        return None
