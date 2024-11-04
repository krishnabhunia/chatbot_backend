import asyncio
import websockets

async def client():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        while True:
            message = "Hello WebSocket!"
            await websocket.send(message)
            print(f"Sent message: {message}")
            
            response = await websocket.recv()
            print(f"Received response: {response}")

            inp = input("Enter message to send: ")
            await websocket.send(inp)
            print(f"Sent message: {inp}")
            
            response = await websocket.recv()
            print(f"Received response: {response}")

asyncio.get_event_loop().run_until_complete(client())
