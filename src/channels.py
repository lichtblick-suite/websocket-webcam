
from src.utils.load_json import load_json 
from foxglove_websocket.server import FoxgloveServer

async def add_channels_to_server(server: FoxgloveServer):
    channels = {}
    
    channels['image'] = await server.add_channel({
        "topic": "/webcam",
        "encoding": "json",
        "schemaName": "foxglove.CompressedImage",
        "schema": load_json('src/schemas/CompressedImage.json'),
        "schemaEncoding": "jsonschema",
    })
    
    channels['camera_calibration'] = await server.add_channel({
        "topic": "/webcam/camera_info",
        "encoding": "json",
        "schemaName": "foxglove.CameraCalibration",
        "schema": load_json('src/schemas/CameraCalibration.json'),
        "schemaEncoding": "jsonschema",
    })
    
    channels['faces'] = await server.add_channel({
        "topic": "/markers/faces",
        "encoding": "json",
        "schemaName": "foxglove.SceneUpdate",
        "schema": load_json('src/schemas/SceneUpdate.json'),
        "schemaEncoding": "jsonschema",
    })
    
    channels['random'] = await server.add_channel({
        "topic": "/random",
        "encoding": "json",
        "schemaName": "foxglove.Random",
        "schema": load_json('src/schemas/RandomValue.json'),
        "schemaEncoding": "jsonschema",
    })
    
    return channels