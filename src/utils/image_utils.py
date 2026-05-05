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
