import json

from src.config import IMAGE_WIDTH, IMAGE_HEIGHT

def get_camera_info_message(timestamp: json): 
    message = {
        "timestamp": timestamp,
        "frame_id": "camera_frame",
        "width": IMAGE_WIDTH,
        "height": IMAGE_HEIGHT,
        "distortion_model": "",
        "D": [0, 0, 0, 0, 0], 
        "K": [
            500.0, 0.0, IMAGE_WIDTH / 2,
            0.0, 500.0, IMAGE_HEIGHT / 2,
            0.0, 0.0, 1.0
        ], 
        "R": [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0
        ],
        "P": [
            500.0, 0.0, IMAGE_WIDTH / 2, 0.0,
            0.0, 500.0, IMAGE_HEIGHT / 2, 0.0,
            0.0, 0.0, 1.0, 0.0
        ] 
    }
    
    return json.dumps(message).encode('utf8')