import asyncio
import websockets


async def handler(websocket, path):
    async def send_messages():
        while True:
            message = input("Msg To client:")
            await websocket.send(message)
            print(f"Sent: {message}")
            await asyncio.sleep(1)  # Sending a message every 3 seconds (adjust as needed)

    async def receive_messages():
        while True:
            async for message in websocket:
                print(f"Received from client: {message}")

    await asyncio.gather(send_messages(), receive_messages())

start_server = websockets.serve(handler, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
