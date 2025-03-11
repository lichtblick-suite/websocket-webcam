import json
import cv2
import numpy as np

# Load a pre-trained face detection model (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Example camera calibration data (replace with actual values from your calibration)
K = np.array([[500.0, 0.0, 960.0], [0.0, 500.0, 540.0], [0.0, 0.0, 1.0]])  # Intrinsic matrix
D = np.array([0, 0, 0, 0, 0])  # Distortion coefficients

# Function to undistort points
def undistort_points(points, K, D):
    points = np.array([points], dtype=np.float32)
    return cv2.undistortPoints(points, K, D)

# Function to convert 2D face center to 3D coordinates
def get_3d_coordinates(face_center, K, D, depth=3.0):
    # Undistort the 2D points using camera intrinsic matrix and distortion coefficients
    undistorted_points = undistort_points(face_center, K, D)
    x_2d, y_2d = undistorted_points[0][0]

    # Assuming depth (Z) is known, project the 2D point to 3D space
    x_3d = (x_2d - K[0][2]) * depth / K[0][0]
    y_3d = (y_2d - K[1][2]) * depth / K[1][1]

    return x_3d, y_3d, depth

# Function to get the faces message
def get_faces_message(frame, timestamp):
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,  # Increase to reduce false positives (try 1.2–1.3)
        minNeighbors=9,    # Increase to require more "confirmations" (try 7–10)
        minSize=(60, 60)   # Ignore very small objects (increase if needed)
    )


    # Create SceneUpdate message with cubes for each face
    scene_update = create_scene_update(faces, timestamp)
    
    return scene_update

# Function to create SceneUpdate with cubes for each face
# Function to create SceneUpdate with cubes for each face
def create_scene_update(faces, timestamp):
    img_width, img_height = 1920, 1080  # Your image dimensions

    cubes = []
    for (x, y, w, h) in faces:
        # Convert pixel coordinates to normalized [-1, 1] range
        x_norm = ((x + w / 2) - (img_width / 2)) / (img_width / 4)  # Normalize X
        y_norm = -((y + h / 2) - (img_height / 2)) / (img_height / 2)  # Normalize Y (inverted)
        
        cube = {
            "color": { "r": 20, "g": 2, "b": 200, "a": 0.1 },
            "size": { "x": w / 500, "y": h / 500, "z": 0.00001 },  # Small cube for visualization
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
        "timestamp": timestamp,
        "entities": [scene_entity]
    }

    return json.dumps(scene_update).encode('utf8')