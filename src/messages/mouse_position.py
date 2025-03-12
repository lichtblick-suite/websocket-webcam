import json
import pyautogui
from screeninfo import get_monitors
from src.config import SCREEN_MONITOR_INDEX

monitor = get_monitors()[SCREEN_MONITOR_INDEX]
screen_width = monitor.width
screen_height = monitor.height

def create_scene_update(x, y, timestamp):

    cube = {
        "color": { "r": 20, "g": 2, "b": 200, "a": 1 },
        "size": { "x": 5, "y": 5, "z": 5 },  # Small cube for visualization
        "pose": {
            "position": {
                "x": float(x),
                "y": float(y),
                "z": float(0),
            },
            "orientation": { "x": 0, "y": 0, "z": 0, "w": 1 },
        }
    }

    scene_entity = {
        "timestamp": timestamp,
        "frame_id": "mouse_frame",
        "frame_locked": True,
        "id": "faces",
        "cubes": [cube],
        "arrows": [],
        "spheres": [],
        "cylinders": [],
        "lines": [],
        "triangles": [],
        "texts": [],
        "models": []
    }

    scene_update = {
        "deletions": [],
        "entities": [scene_entity]
    }
    
    return scene_update

def get_mouse_messages(timestamp: json):
    # Get current mouse position
    x, y = pyautogui.position()

    y = screen_height - y  # Invert Y-axis to match image
    
    x_percent = (x / screen_width) * 100
    y_percent = (y / screen_height) * 100 
    
    message_position = {
        "timestamp": timestamp,
        "x": x,
        "y": y,
    }
    
    message_markers = create_scene_update(x_percent, y_percent, timestamp)
    
    return json.dumps(message_position).encode('utf8'), json.dumps(message_markers).encode('utf8')