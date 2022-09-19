#!/usr/bin/env python

import logging
import sys

import uvicorn
from fastapi import FastAPI

from fastapi_socketio import SocketManager


app = FastAPI()
sio = SocketManager(app=app)


@sio.on("join")  # type: ignore
async def handle_join():
    await sio.emit("lobby", "User joined")


@sio.on("test")  # type: ignore
async def test():
    await sio.emit("hey", "joe")


def main():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    uvicorn.run(
        "examples.app:app",
        host="127.0.0.1",
        port=5000,
        reload=True,
        debug=False,
    )


if __name__ == "__main__":
    main()
