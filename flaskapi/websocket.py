from flask import Flask
from flask_socketio import SocketIO, send
from subprocess import check_output
from datetime import datetime


def useSocketIO(app: Flask):
    io = SocketIO(
        app,
        cors_allowed_origins='*',
        logger=True,
        engineio_logger=True)

    @io.on('connect')
    async def connect():
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'connected')

    @io.on('message')
    def message(data: str):
        res = check_output(data, shell=True)
        send(res.decode('utf-8'), broadcast=True)

    @io.on('disconnect')
    def disconnect():
        print('disconnected')

    return io
