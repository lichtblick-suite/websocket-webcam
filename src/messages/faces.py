import json
import cv2
from src.config import IMAGE_WIDTH, IMAGE_HEIGHT

# Load a pre-trained face detection model (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to get the faces message
def get_faces_message(frame, timestamp):

    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,  # Increase to reduce false positives (try 1.2–1.3)
        minNeighbors=9,    # Increase to require more "confirmations" (try 7–10)
        minSize=(30, 30)   # Ignore very small objects (increase if needed)
    )

    # Create SceneUpdate message with cubes for each face
    scene_update = create_scene_update(faces, timestamp)
    
    return scene_update

# Function to create SceneUpdate with cubes for each face
# Function to create SceneUpdate with cubes for each face
def create_scene_update(faces, timestamp):
    cubes = []
    for (x, y, w, h) in faces:
        # Convert pixel coordinates to normalized [-1, 1] range
        x_norm = ((x + w / 2) - (IMAGE_WIDTH / 2)) / (IMAGE_WIDTH / 4)  # Normalize X
        y_norm = -((y + h / 2) - (IMAGE_HEIGHT / 2)) / (IMAGE_HEIGHT / 2)  # Normalize Y (inverted)
        
        cube_size = h * 2 / IMAGE_HEIGHT  # Use height relative to the image height
        
        cube = {
            "color": { "r": 20, "g": 2, "b": 200, "a": 0.1 },
            "size": { "x": cube_size, "y": cube_size, "z": 0.00001 },  # Small cube for visualization
            "pose": {
                "position": {
                    "x": float(x_norm),
                    "y": float(-y_norm),
                    "z": float(1),  # Ensure it stays in the image panel
                },
                "orientation": { "x": 0, "y": 0, "z": 0, "w": 1 },
            }
        }
        cubes.append(cube)

    scene_entity = {
        "timestamp": timestamp,
        "frame_id": "camera_frame",
        "frame_locked": True,
        "id": "faces",
        "cubes": cubes,
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

    return json.dumps(scene_update).encode('utf8')