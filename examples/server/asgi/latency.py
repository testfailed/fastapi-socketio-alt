#!/usr/bin/env python

import logging
import sys

import socketio
import uvicorn


sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=["http://127.0.0.1:5000"],
)
app = socketio.ASGIApp(
    sio,
    # socketio_path="socket.io",
    static_files={
        "/": "static/latency.html",
        "/static": "static",
    },
)


@sio.event
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


def main():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    uvicorn.run(
        "examples.server.asgi.latency:app",
        host="127.0.0.1",
        port=5000,
        reload=True,
        debug=False,
    )


if __name__ == "__main__":
    main()
