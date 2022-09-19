#!/usr/bin/env python

import time
import socketio


sio = socketio.Client(logger=True, engineio_logger=True)
start_timer: float


def send_ping():
    global start_timer
    start_timer = time.time()
    sio.emit("ping_from_client")


@sio.event
def connect():
    print("connected to server")
    send_ping()


@sio.event
def pong_from_server(data):
    print(f"pong_from_server (sid=${data['sid']}, room=${data['room']})")
    global start_timer
    latency = time.time() - start_timer
    print("latency is {0:.2f} ms".format(latency * 1000))
    sio.sleep(1)
    if sio.connected:
        send_ping()


def main():
    sio.connect("http://127.0.0.1:5000")
    sio.wait()


if __name__ == "__main__":
    main()
