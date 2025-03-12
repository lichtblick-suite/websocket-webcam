import asyncio
import time
import cv2
from src.config import IMAGE_WIDTH, IMAGE_HEIGHT, WEBCAM_INDEX
from src.messages.mouse_position import get_mouse_messages
from src.messages.eyes import get_eyes_message
from src.messages.faces import get_faces_message
from src.messages.camera_info import get_camera_info_message
from src.messages.webcam import get_image_message
from src.channels import add_channels_to_server
from src.listener import FoxgloveListener
from foxglove_websocket import run_cancellable
from foxglove_websocket.server import FoxgloveServer

async def main():
    # Open the webcam (0 is the default camera)
    cap = cv2.VideoCapture(WEBCAM_INDEX)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
       
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)
    
    async with FoxgloveServer(
        "0.0.0.0",
        8765,
        "example server",
        capabilities=["clientPublish", "services"],
        supported_encodings=["json"],
    ) as server:
        server.set_listener(FoxgloveListener())
        
        channels = await add_channels_to_server(server)
    
        # Send frames continuously
        i = 0
        while True:            
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture image.")
                break

            frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
            
            # Encode frame as JPEG and then base64 encode it to send as string
            ret, jpeg = cv2.imencode('.jpg', frame)
            if ret:
                await asyncio.sleep(0.001)

                # Send the same Timestamp
                timestamp = { "sec": int(time.time()), "nsec": int((time.time() % 1) * 1e9)}
            
                image_message = get_image_message(jpeg, timestamp)
                await server.send_message(channels['image'], time.time_ns(), image_message)
                
                camera_info_message = get_camera_info_message(timestamp)
                await server.send_message(channels['camera_calibration'], time.time_ns(), camera_info_message)
                
                faces_message = get_faces_message(frame, timestamp)
                await server.send_message(channels['faces'], time.time_ns(), faces_message)
                
                eyes_message = get_eyes_message(frame, timestamp)
                await server.send_message(channels['eyes'], time.time_ns(), eyes_message)
                
                mouse_position_message, mouse_markers_message = get_mouse_messages(timestamp)
                await server.send_message(channels["mouse_position"], time.time_ns(), mouse_position_message)
                await server.send_message(channels["mouse_markers"], time.time_ns(), mouse_markers_message)
                
                

        cap.release()

if __name__ == "__main__":
    run_cancellable(main())
