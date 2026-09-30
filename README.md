# Distributed Market Data Processor

## Assignment Details
* **Student Name:** [Your Name]
* **Student Roll Number:** [Your Roll Number]
* **Email ID:** bulusaw0003@gmail.com
* **Assignment Application Name:** Distributed Market Data Processor
* **Application Description:** A distributed cloud application that ingests real-time financial market data, processes it concurrently for algorithmic trading feature engineering, and stores the structured data for downstream ML models.

## Technical Specifications
* **Architecture Used:** Microservices
* **Communication Mechanism:** WebSocket (Data ingestion) & REST API (Internal service communication)
* **Data Storage Type & Technology:** SQL / PostgreSQL
* **Computing Type:** Distributed / Cloud
* **Technology Stack / Framework Used:** Python, FastAPI, PostgreSQL, Uvicorn, WebSockets.

## Architecture Diagram
![Architecture Diagram](./assets/watermarked_img_10363661139061782359.png)

## How to Run Locally
1. Start the Processing Service (Port 8001):
   `cd processing_service`
   `uvicorn main:app --port 8001 --reload`
2. Start the Ingestion Service (Port 8000):
   `cd ingestion_service`
   `uvicorn main:app --port 8000 --reload`