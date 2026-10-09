import asyncio
import websockets

async def send_test_data():
    uri = "ws://localhost:8000/ws/market-data"
    async with websockets.connect(uri) as websocket:
        print("Connected to Ingestion Service!")

        # Send a fake market tick
        test_payload = "BTC/USD: 64500"
        await websocket.send(test_payload)
        print(f"Sent: {test_payload}")

        # Wait for confirmation from the processing service
        response = await websocket.recv()
        print(f"Received back: {response}")

asyncio.run(send_test_data())