#!/usr/bin/env python

import logging
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from fastapi_socketio import SocketManager


"""
FastAPI Routers
"""


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def get_main():
    return FileResponse("static/latency.html", media_type="text/html")


"""
FastAPI-SocketIO
"""


sio = SocketManager(app=app)


@sio.on("ping_from_client")  # type: ignore
async def ping_from_client(sid):
    print(f"ping_from_client (sid=${sid})")
    await sio.emit(
        "pong_from_server",
        {
            "sid": sid,
            "room": sid,
        },
        room=sid,
    )


"""
Uvicorn Server
"""


def main():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    uvicorn.run(
        "examples.server.fastapi.latency:app",
        host="127.0.0.1",
        port=5000,
        reload=True,
        debug=False,
    )


if __name__ == "__main__":
    main()
