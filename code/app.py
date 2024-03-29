from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rooms.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    available = db.Column(db.Boolean, default=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    if 'username' in session:
        rooms = Room.query.all()
        return render_template('index.html', rooms=rooms)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = "Неправильное имя или пароль. Повторите попытку."
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/book', methods=['POST'])
def book():
    if 'username' not in session:
        return redirect(url_for('login'))
    room_id = int(request.form['room_id'])
    room = Room.query.get(room_id)
    if room.available:
        room.available = False
        db.session.commit()
        return f"Комната {room_id} была забронирована успешно!"
    else:
        return "Извините, выбранная комната недоступна."

# Обработчики ошибок
@app.errorhandler(400)
def bad_request_error(error):
    return render_template('error.html', error_code=400, error_message="Bad Request"), 400

@app.errorhandler(401)
def unauthorized_error(error):
    return render_template('error.html', error_code=401, error_message="Unauthorized"), 401

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('error.html', error_code=403, error_message="Forbidden"), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, error_message="Internal Server Error"), 500

@app.errorhandler(502)
def bad_gateway_error(error):
    return render_template('error.html', error_code=502, error_message="Bad Gateway"), 502

@app.errorhandler(503)
def service_unavailable_error(error):
    return render_template('error.html', error_code=503, error_message="Service Unavailable"), 503

@app.errorhandler(505)
def http_version_not_supported_error(error):
    return render_template('error.html', error_code=505, error_message="HTTP Version Not Supported"), 505

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)