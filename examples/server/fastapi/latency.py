#!/usr/bin/env python

import logging
import sys

import uvicorn
from fastapi import FastAPI

from fastapi_socketio import SocketManager


app = FastAPI()
sio = SocketManager(app=app)


@sio.on("ping_from_client")  # type: ignore
async def ping_from_client(sid):
    print(f"ping_from_client (sid=${sid})")
    await sio.emit("pong_from_server", sid)


def main():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    uvicorn.run(
        "examples.server.fastapi.latency:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        debug=False,
    )


if __name__ == "__main__":
    main()
