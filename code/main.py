from flask import Flask, render_template, request

app = Flask(_name_)

# Типа база данных, потом поменять на sql
rooms = {
    1: {'name': 'Room 101', 'available': True},
    2: {'name': 'Room 102', 'available': True},
    3: {'name': 'Room 103', 'available': True}
}

@app.route('/')
def index():
    return render_template('index.html', rooms=rooms)

@app.route('/book', methods=['POST'])
def book():
    room_id = int(request.form['room_id'])
    if room_id in rooms and rooms[room_id]['available']:
        rooms[room_id]['available'] = False
        return f"Room {room_id} has been booked successfully!"
    else:
        return "Sorry, the selected room is not available."

if _name_ == '_main_':
    app.run(debug=True)