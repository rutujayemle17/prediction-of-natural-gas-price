from flask import Flask, request, render_template, redirect, url_for, session
import pickle
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'rutuja17'

# Load the trained model
model = pickle.load(open('gas.pkl', 'rb'))

# Dummy database for users (in a real application, use a proper database)
users = {}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('prediction'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            return redirect(url_for('prediction'))
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        if username in users:
            return render_template('register.html', error='Username already exists')
        
        users[username] = {'password': generate_password_hash(password)}
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            year = int(request.form['year'])
            month = int(request.form['month'])
            day = int(request.form['day'])
            
            features = [year, month, day]
            prediction = model.predict([features])[0]
            
            return render_template('index.html', prediction_text=f'Predicted Natural Gas Price: ${prediction:.2f}')
        except Exception as e:
            return render_template('index.html', prediction_text=f'Error: {str(e)}')
    
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
