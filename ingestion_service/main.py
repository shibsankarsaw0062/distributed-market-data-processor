from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import httpx
import asyncio
import json

app = FastAPI(title="Ingestion Microservice")

# URL of our internal processing service
PROCESSING_SERVICE_URL = "http://localhost:8001/process"

@app.websocket("/ws/market-data")
async def market_data_endpoint(websocket: WebSocket):
    await websocket.accept() # Accept the WebSocket connection
    try:
        while True:
            # Wait to receive a message (simulating incoming live data)
            data = await websocket.receive_text()
            payload = {"raw_data": data}
            
            # Forward the data to the processing service via REST API
            async with httpx.AsyncClient() as client:
                response = await client.post(PROCESSING_SERVICE_URL, json=payload)
                
            # Send confirmation back to the websocket client
            await websocket.send_text(f"Processed: {response.json()}")
            
    except WebSocketDisconnect:
        print("Market data feed disconnected.")