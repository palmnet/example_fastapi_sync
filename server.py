import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/wait")
def wait():
    # 数十秒間待機
    time.sleep(20)  # 20秒待機
    return {"message": "Waited for 20 seconds"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
