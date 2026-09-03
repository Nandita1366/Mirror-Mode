import asyncio
import websockets
import json

async def test():
    uri = "ws://127.0.0.1:8000/ws/interview/test-session-1"
    async with websockets.connect(uri) as websocket:
        # Send a fake "evaluate" text message
        await websocket.send(json.dumps({
            "type": "evaluate",
            "question": "What is a REST API?",
            "transcript": "A REST API is an architectural style for web services using HTTP methods."
        }))

        response = await websocket.recv()
        print("Received:", response)

asyncio.run(test())