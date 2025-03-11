import json

def get_camera_info_message(timestamp: json): 
    message = {
        "timestamp": timestamp,
        "frame_id": "camera_frame",
        "width": 1920,
        "height": 1080,
        "distortion_model": "",
        "D": [0, 0, 0, 0, 0], 
        "K": [
            500.0, 0.0, 960.0,
            0.0, 500.0, 540.0,
            0.0, 0.0, 1.0
        ], 
        "R": [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0
        ],
        "P": [
            500.0, 0.0, 960.0, 0.0,
            0.0, 500.0, 540.0, 0.0,
            0.0, 0.0, 1.0, 0.0
        ] 
    }
    
    return json.dumps(message).encode('utf8')