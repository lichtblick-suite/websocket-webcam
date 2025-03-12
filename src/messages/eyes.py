import json
import cv2
from src.config import IMAGE_WIDTH, IMAGE_HEIGHT

# Load a pre-trained eye detection model (Haar Cascade)
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Function to get the eyes message
def get_eyes_message(frame, timestamp):
    
    # Convert to grayscale for eye detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes in the image
    eyes = eye_cascade.detectMultiScale(
        gray,
        scaleFactor=1.5,  # Increase to reduce false positives (try 1.2–1.3)
        minNeighbors=9,    # Increase to require more "confirmations" (try 7–10)
        minSize=(15, 15)   # Ignore very small objects (increase if needed)
    )

    # Create SceneUpdate message with cubes for each eye
    scene_update = create_scene_update(eyes, timestamp)
    
    return scene_update

# Function to create SceneUpdate with spheres for each eye
def create_scene_update(eyes, timestamp):

    spheres = []  # Use spheres instead of cubes
    for (x, y, w, h) in eyes:
        # Convert pixel coordinates to normalized [-1, 1] range
        x_norm = ((x + w / 2) - (IMAGE_WIDTH / 2)) / (IMAGE_WIDTH / 4)  # Normalize X
        y_norm = -((y + h / 2) - (IMAGE_HEIGHT / 2)) / (IMAGE_HEIGHT / 2)  # Normalize Y (inverted)
        
        cube_size_x = w * 2 / IMAGE_WIDTH  # Use width relative to the image width
        
        sphere = {
            "color": { "r": 200, "g": 2, "b": 20, "a": 0.3 },
            "size": { "x": cube_size_x, "y": cube_size_x, "z": 0.00001 },  # Small cube for visualization
            "pose": {
                "position": {
                    "x": float(x_norm),
                    "y": float(-y_norm),
                    "z": float(1),  # Ensure it stays in the image panel
                },
                "orientation": { "x": 0, "y": 0, "z": 0, "w": 1 },
            }
        }
        spheres.append(sphere)

    scene_entity = {
        "timestamp": timestamp,
        "frame_id": "camera_frame",
        "frame_locked": True,
        "id": "eyes",
        "spheres": spheres,  # Use spheres here instead of cubes
        "arrows": [],
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

    return json.dumps(scene_update).encode('utf8')
