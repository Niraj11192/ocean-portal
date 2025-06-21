from flask import Flask, render_template, request, redirect, session, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store users and submissions
users = {'gobardhan': '1234'}
submissions = []

@app.route('/')
def index():
    query = request.args.get('q', '').lower()
    if query:
        filtered = [s for s in submissions if query in s['title'].lower() or query in s['abstract'].lower() or query in s['user'].lower()]
    else:
        filtered = submissions
    return render_template('index.html', submissions=filtered)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users and users[uname] == pwd:
            session['user'] = uname
            return redirect('/upload')
        return "Invalid credentials!"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users:
            return "User already exists!"
        users[uname] = pwd
        return redirect('/login')
    return render_template('register.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        title = request.form['title']
        abstract = request.form['abstract']
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)
            submissions.append({
                'title': title,
                'abstract': abstract,
                'filename': filename,
                'user': session['user']
            })
            return redirect('/')
    return render_template('upload.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', submissions=submissions)

@app.route('/download/<filename>')
def download(filename):
    return redirect(url_for('static', filename=f'../uploads/{filename}'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
    
if __name__ == '__main__':
    app.run(debug=True)
