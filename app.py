from flask import Flask, request, redirect, url_for, render_template, jsonify, session, flash
import os
import datetime
import hashlib
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'jpg', 'jpeg', 'png', 'mp3', 'mkv'}  # Updated allowed extensions
SERVER_IP = '192.168.68.101'
SERVER_PORT = '5000'
PASSWORD = 'MegaGay1213'
USERS_FILE = 'users.json'
UPLOAD_LOG = 'upload_log.json'

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
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        users = load_users()
        if email in users and users[email]['password'] == password:
            session['username'] = users[email]['username']
            flash('Login successful!', 'success')
            return redirect(url_for('upload_file'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if email in users:
            flash('Email already registered. Please login or use a different email.', 'warning')
            return redirect(url_for('login'))
        users[email] = {'username': username, 'password': hash_password(password)}
        save_users(users)
        flash('Sign up successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'username' not in session:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        ip = request.form['server_ip']
        port = request.form['server_port']
        password = request.form['password']
        
        if ip != SERVER_IP or port != SERVER_PORT or password != PASSWORD:
            flash('Invalid credentials. Please try again.', 'danger')
            return render_template('upload.html')
        
        if 'file' not in request.files:
            flash('No file part.', 'danger')
            return render_template('upload.html')
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file.', 'danger')
            return render_template('upload.html')
        
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
            
            flash('File successfully uploaded.', 'success')
            return redirect(url_for('upload_file'))
        else:
            flash('File type not allowed.', 'danger')
            return render_template('upload.html')
    
    return render_template('upload.html')

@app.route('/recent_files', methods=['GET'])
def recent_files():
    log = load_upload_log()
    return jsonify(log)

if __name__ == '__main__':
    app.run(host=SERVER_IP, port=int(SERVER_PORT), debug=True)
