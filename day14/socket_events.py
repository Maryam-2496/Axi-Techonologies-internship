from flask_socketio import emit, join_room
from extensions import socketio
import jwt
import os
from flask import request
from flask_socketio import disconnect

print("socket_events.py has been loaded!", flush=True)


@socketio.on("connect")
def handle_connect():
    token = request.args.get("token")

    if not token:
        print("Connection rejected: no token provided", flush=True)
        disconnect()
        return False

    try:
        payload = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
        print(f"Client connected: user_id={payload['userId']}", flush=True)
        emit("server_message", {"msg": "Welcome! You are connected and authenticated."})
    except jwt.ExpiredSignatureError:
        print("Connection rejected: token expired", flush=True)
        disconnect()
        return False
    except jwt.InvalidTokenError:
        print("Connection rejected: invalid token", flush=True)
        disconnect()
        return False


@socketio.on("disconnect")
def handle_disconnect():
    print("A client disconnected.", flush=True)


@socketio.on_error_default
def handle_error(e):
    print(f"SocketIO error occurred: {e}", flush=True)
    emit("server_message", {"msg": "An error occurred. Please try again."})


@socketio.on("join_room")
def handle_join_room(data):
    room = data.get("room")
    join_room(room)
    print(f"Client joined room: {room}", flush=True)
    emit("server_message", {"msg": f"You joined room {room}"}, to=room)


@socketio.on("send_message")
def handle_send_message(data):
    room = data.get("room")
    message = data.get("message")
    print(f"Message in room {room}: {message}", flush=True)
    emit("receive_message", {"message": message}, to=room)
