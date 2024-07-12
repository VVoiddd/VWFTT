from flask import Flask, request, redirect, url_for, render_template, jsonify
import os
import datetime
import hashlib
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4'}
SERVER_IP = 'IP'
SERVER_PORT = 'PORT'
PASSWORD = 'your_password'
USERS_FILE = 'users.json'  # File to store user info

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

# Hash password with SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
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
                return 'File successfully uploaded'
        else:
            return 'Invalid credentials'
    return render_template('upload.html')

@app.route('/recent_files', methods=['GET'])
def recent_files():
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            modified_time = os.path.getmtime(file_path)
            files.append({
                'filename': filename,
                'uploaded_at': datetime.datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')
            })
    return jsonify(files)

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return 'Email and password are required'
    
    hashed_password = hash_password(password)
    users = load_users()
    if email in users:
        return 'Email already registered'
    
    users[email] = hashed_password
    save_users(users)
    return 'User registered successfully'

if __name__ == '__main__':
    app.run(host=SERVER_IP, port=int(SERVER_PORT), debug=True)
