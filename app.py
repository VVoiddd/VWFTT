from flask import Flask, request, redirect, url_for, render_template, jsonify, session
import os
import datetime
import hashlib
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4'}
SERVER_IP = 'IP'
SERVER_PORT = '5000'
PASSWORD = 'your_password'
USERS_FILE = 'users.json'  # File to store user info
UPLOAD_LOG = 'upload_log.json'  # File to store upload log

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load users from JSON file
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

# Save users to JSON file
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

# Load upload log from JSON file
def load_upload_log():
    if not os.path.exists(UPLOAD_LOG):
        return []
    with open(UPLOAD_LOG, 'r') as f:
        return json.load(f)

# Save upload log to JSON file
def save_upload_log(log):
    with open(UPLOAD_LOG, 'w') as f:
        json.dump(log, f)

# Hash password with SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('upload_file'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        users = load_users()
        if email in users and users[email]['password'] == password:
            session['username'] = users[email]['username']
            return redirect(url_for('upload_file'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if email in users:
            return 'Email already registered'
        users[email] = {'username': username, 'password': hash_password(password)}
        save_users(users)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        ip = request.form['server_ip']
        port = request.form['server_port']
        password = request.form['password']
        if ip == SERVER_IP and port == SERVER_PORT and password == PASSWORD:
            if 'file' not in request.files:
                return 'No file part'
            file = request.files['file']
            if file.filename == '':
                return 'No selected file'
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                log = load_upload_log()
                log.append({
                    'filename': filename,
                    'uploaded_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'uploaded_by': session['username']
                })
                save_upload_log(log)
                return 'File successfully uploaded'
        else:
            return 'Invalid credentials'
    return render_template('upload.html')

@app.route('/recent_files', methods=['GET'])
def recent_files():
    log = load_upload_log()
    return jsonify(log)

if __name__ == '__main__':
    app.run(host=SERVER_IP, port=int(SERVER_PORT), debug=True)
