import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

import requests
from fastapi import FastAPI, Request

app = FastAPI()
# Configure logging with datetime and log level
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Create a ThreadPoolExecutor with a suitable max_workers value
executor = ThreadPoolExecutor(max_workers=5)


def sync_http_request():
    logging.info("Making a synchronous HTTP request")
    response = requests.get("http://localhost:8001/wait")
    logging.info("Response received")
    return response.json()


async def async_http_request():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, sync_http_request)


@app.get("/")
async def read_root():
    # Use run_in_executor to execute the synchronous HTTP request function
    response = await asyncio.get_event_loop().run_in_executor(
        executor, sync_http_request
    )
    return {"response": response}


@app.get("/sync")
async def read_sync():
    sync_http_request()


@app.get("/fire")
async def fire_sync():
    asyncio.create_task(async_http_request())
    return {"message": "Request has been fired off"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
