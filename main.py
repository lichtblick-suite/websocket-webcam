import asyncio
import time
import cv2
from src.messages.random_value import get_random_value_message
from src.messages.faces import get_faces_message
from src.messages.camera_info import get_camera_info_message
from src.messages.webcam import get_image_message
from src.channels import add_channels_to_server
from src.listener import FoxgloveListener
from foxglove_websocket import run_cancellable
from foxglove_websocket.server import FoxgloveServer

async def main():
    # Open the webcam (0 is the default camera)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
       
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

            # Encode frame as JPEG and then base64 encode it to send as string
            ret, jpeg = cv2.imencode('.jpg', frame)
            if ret:
                await asyncio.sleep(0.01)

                # Send the same Timestamp
                timestamp = { "sec": int(time.time()), "nsec": int((time.time() % 1) * 1e9)}
            
                image_message = get_image_message(jpeg, timestamp)
                await server.send_message(channels['image'], time.time_ns(), image_message)
                
                camera_info_message = get_camera_info_message(timestamp)
                await server.send_message(channels['camera_calibration'], time.time_ns(), camera_info_message)
                
                faces_message = get_faces_message(frame, timestamp)
                await server.send_message(channels['faces'], time.time_ns(), faces_message)
                
                random_value_message = get_random_value_message(timestamp)
                await server.send_message(channels["random"], time.time_ns(), random_value_message)

        cap.release()

if __name__ == "__main__":
    run_cancellable(main())
