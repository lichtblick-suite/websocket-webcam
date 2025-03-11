import base64
import json

def get_image_message(jpeg, timestamp: json):
    encoded_image = base64.b64encode(jpeg).decode('utf-8')
    
    message = {
        "timestamp": timestamp,
        "frame_id": "camera_frame",
        "data": encoded_image,
        "format": "jpeg"    
    }
    
    return json.dumps(message).encode('utf8')