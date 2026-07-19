from fastapi import FastAPI
from pathlib import Path
import uvicorn
import chatify.config
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


if __name__ == "__main__":
    chatify.config.load(Path(__file__).parent)

    uvicorn.run(
        app=app,
        host=chatify.config.get().host,
        port=chatify.config.get().port
    )