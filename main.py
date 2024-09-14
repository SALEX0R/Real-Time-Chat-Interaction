from flask import Flask, render_template, request, session, redirect, url_for, send_file
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
from main_rag import generate_text_from_llm, text_to_speech 
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "ABRAKADVRA"
socketio = SocketIO(app)

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code

@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        if not name:
            return render_template("home.html", error="Please enter your name", code=code, name=name)
        if join != False and not code:
            return render_template("home.html", error="Please enter room code", code=code, name=name)
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room not found.", code=code, name=name)
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))
    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))
    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    user_message = data["data"]
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = {
        "name": session.get("name"),
        "message": user_message,
        "timestamp": timestamp
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {user_message}")

    # Generate LLM response
    llm_response = generate_text_from_llm(user_message)
    content = {
        "name": "LLM",
        "message": llm_response,
        "timestamp": timestamp
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"LLM said: {llm_response}")

@app.route("/speak/<message>")
def speak(message):
    audio_path = text_to_speech(message)
    return send_file(audio_path, as_attachment=True)

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    join_room(room)
    send({"name": name, "message": "has joined the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined the room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)
    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

if __name__ == "__main__":
    socketio.run(app, debug=True)
