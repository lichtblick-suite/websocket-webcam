import asyncio
import json
import time
import cv2
import base64
from foxglove.schemas import CompressedImage
from foxglove_websocket import run_cancellable
from foxglove_websocket.server import FoxgloveServer, FoxgloveServerListener
from foxglove_websocket.types import (
    ChannelId,
    ClientChannel,
    ClientChannelId,
    ServiceId,
)

async def main():
    # Open the webcam (0 is the default camera)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    class Listener(FoxgloveServerListener):
        async def on_subscribe(self, server: FoxgloveServer, channel_id: ChannelId):
            print("First client subscribed to", channel_id)

        async def on_unsubscribe(self, server: FoxgloveServer, channel_id: ChannelId):
            print("Last client unsubscribed from", channel_id)

        async def on_client_advertise(
            self, server: FoxgloveServer, channel: ClientChannel
        ):
            print("Client advertise:", json.dumps(channel))

        async def on_client_unadvertise(
            self, server: FoxgloveServer, channel_id: ClientChannelId
        ):
            print("Client unadvertise:", channel_id)

        async def on_client_message(
            self, server: FoxgloveServer, channel_id: ClientChannelId, payload: bytes
        ):
            msg = json.loads(payload)
            print(f"Client message on channel {channel_id}: {msg}")

        async def on_service_request(
            self,
            server: FoxgloveServer,
            service_id: ServiceId,
            call_id: str,
            encoding: str,
            payload: bytes,
        ) -> bytes:
            if encoding != "json":
                return json.dumps(
                    {"success": False, "error": f"Invalid encoding {encoding}"}
                ).encode()

            request = json.loads(payload)
            if "data" not in request:
                return json.dumps(
                    {"success": False, "error": f"Missing key 'data'"}
                ).encode()

            print(f"Service request on service {service_id}: {request}")
            return json.dumps(
                {"success": True, "message": f"Received boolean: {request['data']}"}
            ).encode()

    async with FoxgloveServer(
        "0.0.0.0",
        8765,
        "example server",
        capabilities=["clientPublish", "services"],
        supported_encodings=["json"],
    ) as server:
        server.set_listener(Listener())
        chan_id = await server.add_channel(
            {
                "topic": "/webcam",
                "encoding": "json",
                "schemaName": "foxglove.CompressedImage",
                "schema": json.dumps(
                    {
                        "type": "object",
                        "properties": {    "timestamp": {
      "type": "object",
      "title": "time",
      "properties": {
        "sec": {
          "type": "integer",
          "minimum": 0
        },
        "nsec": {
          "type": "integer",
          "minimum": 0,
          "maximum": 999999999
        }
      },
      "description": "Timestamp of image"
    },
    "frame_id": {
      "type": "string",
      "description": "Frame of reference for the image. The origin of the frame is the optical center of the camera. +x points to the right in the image, +y points down, and +z points into the plane of the image."
    },
    "data": {
      "type": "string",
      "contentEncoding": "base64",
      "description": "Compressed image data"
    },
    "format": {
      "type": "string",
      "description": "Image format\n\nSupported values: image media types supported by Chrome, such as `webp`, `jpeg`, `png`"
    }

                        },
                    }
                ),
                "schemaEncoding": "jsonschema",
            }
        )

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
                encoded_image = base64.b64encode(jpeg).decode('utf-8')

                i += 1
                await asyncio.sleep(0.001)
                # Send image as part of the message
                timestamp_sec = int(time.time())
                timestamp_nsec = int((time.time() % 1) * 1e9)  
                message = json.dumps({
                    "timestamp": {
                        "sec": timestamp_sec,
                        "nsec": timestamp_nsec
                    },
                    "frame_id": "camera",
                    "data": encoded_image,
                    "format": "jpeg"    
                }).encode("utf8")
                await server.send_message(chan_id, time.time_ns(), message)

        cap.release()

if __name__ == "__main__":
    run_cancellable(main())
