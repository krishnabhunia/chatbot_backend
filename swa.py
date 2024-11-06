import asyncio
import websockets


async def client():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:

        async def send_messages():
            while True:
                message = input("Msg to server:")
                await websocket.send(message)
                print(f"Sent: {message}")
                await asyncio.sleep(1)  # Sending a message every 3 seconds (adjust as needed)

        async def receive_messages():
            while True:
                async for message in websocket:
                    print(f"Received from server: {message}")

        await asyncio.gather(send_messages(), receive_messages())

asyncio.get_event_loop().run_until_complete(client())
asyncio.get_event_loop().run_forever()
