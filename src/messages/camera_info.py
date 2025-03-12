import json

from src.config import IMAGE_WIDTH, IMAGE_HEIGHT

def get_camera_info_message(timestamp: json): 
    
    # You can define a default focal length, for instance, 500 for 1920x1080
    DEFAULT_FOCAL_LENGTH = 500.0
    ORIGINAL_WIDTH = 1920
    ORIGINAL_HEIGHT = 1080

    # Calculate the scaled focal length based on the image resolution
    scaled_focal_length_x = DEFAULT_FOCAL_LENGTH * (IMAGE_WIDTH / ORIGINAL_WIDTH)
    scaled_focal_length_y = DEFAULT_FOCAL_LENGTH * (IMAGE_HEIGHT / ORIGINAL_HEIGHT)
    
    message = {
        "timestamp": timestamp,
        "frame_id": "camera_frame",
        "width": IMAGE_WIDTH,
        "height": IMAGE_HEIGHT,
        "distortion_model": "",
        "D": [0, 0, 0, 0, 0], 
        "K": [
            scaled_focal_length_x, 0.0, IMAGE_WIDTH / 2,
            0.0, scaled_focal_length_y, IMAGE_HEIGHT / 2,
            0.0, 0.0, 1.0
        ], 
        "R": [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0
        ],
        "P": [
            scaled_focal_length_x, 0.0, IMAGE_WIDTH / 2, 0.0,
            0.0, scaled_focal_length_y, IMAGE_HEIGHT / 2, 0.0,
            0.0, 0.0, 1.0, 0.0
        ] 
    }
    
    return json.dumps(message).encode('utf8')