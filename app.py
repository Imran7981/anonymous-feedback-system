import os
import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from database import init_db, insert_feedback, get_feedback_count, get_all_feedbacks
from datetime import datetime 
from datetime import timedelta
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_section_lifetime = timedelta(minutes=1)
ADMIN_USERNAME = 'imran'
ADMIN_PASSWORD = 'imran1234'

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

# Folder for uploaded media files (store in static/uploads)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize the SQLite database
init_db()

# Home route
@app.route('/index')
def index():
    return render_template('index.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        session['username'] = username
        session['password'] = password
        return redirect(url_for('index'))
    return render_template('login.html')

# Feedback form
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        feedback_text = request.form.get('feedback')
        media_file = request.files.get('media')

        media_filename = None
        if media_file and media_file.filename != '':
            media_filename = secure_filename(media_file.filename)
            media_path = os.path.join(app.config['UPLOAD_FOLDER'], media_filename)
            media_file.save(media_path)

        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save into DB with timestamp
        insert_feedback(session['username'], feedback_text, media_filename, timestamp)
        return redirect(url_for('thank_you'))
        
    return render_template('feedback.html')

# Thank You page
@app.route('/thank_you')
def thank_you():
    count = get_feedback_count()
    return render_template('thank_you.html')

# Serve uploaded media
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete_feedback/<int:feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    conn = sqlite3.connect('feedbacks.db')  # apne database connection function ka use karo
    cursor = conn.cursor()
    cursor.execute("DELETE FROM feedbacks WHERE id = ?", (feedback_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))  # jahan tum admin dashboard ka route rakhe ho

 # Admin dashboard
@app.route('/admin')
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for('admin_login'))

    search = request.args.get('search', '')
    sentiment = request.args.get('sentiment', '')
    sort_order = request.args.get('sort', 'desc')

    conn = sqlite3.connect('feedbacks.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = "SELECT * FROM feedbacks WHERE 1=1"
    params = []

    if search:
        query += " AND (username LIKE ? OR feedback LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    if sentiment:
        query += " AND sentiment = ?"
        params.append(sentiment)
    query += f" ORDER BY timestamp {sort_order.upper()}"

    c.execute(query, params)
    feedbacks = c.fetchall()
    conn.close()

    return render_template("admin.html", feedbacks=feedbacks)
if __name__ == '__main__':
    app.run(debug=True)