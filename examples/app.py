import logging
import sys

import uvicorn
from fastapi import FastAPI

from fastapi_socketio import SocketManager


app = FastAPI()
sio = SocketManager(app=app)


@app.sio.on("join")  # type: ignore
async def handle_join(sid, *args, **kwargs):
    await sio.emit("lobby", "User joined")


# @sio.on("test")
@app.sio.on("test")  # type: ignore
async def test(sid, *args, **kwargs):
    await sio.emit("hey", "joe")


def main():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    uvicorn.run("examples.app:app", host="0.0.0.0", port=8000, reload=True, debug=False)


if __name__ == "__main__":
    main()
