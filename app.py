from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import bcrypt

app = Flask(__name__, static_folder='static', template_folder='templates')

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# MongoDB connection
mongo_uri = "mongodb+srv://harishbhalaa:harish@backend.w8koxqb.mongodb.net/test"
client = MongoClient(mongo_uri)
db = client.test  # Assuming 'test' is the name of your database
collection = db.tech_doctors  # Assuming 'tech_doctors' is the name of your collection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def signin():
    doctor_id = request.form['doctor_id']
    password = request.form['password'].encode('utf-8')

    # Retrieve the user from the database
    user = collection.find_one({'doctor_id': doctor_id})

    if user:
        # Check if the provided password matches the hashed password stored in the database
        if bcrypt.checkpw(password, user['password'].encode('utf-8')):
            # Store the doctor_id in session to track the logged-in user
            session['doctor_id'] = doctor_id
            return redirect(url_for('dashboard'))

    # Display error message as popup alert message using JavaScript
    return render_template('index.html', error="Invalid doctor_id or password", show_alert=True)

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'doctor_id' in session:
        #return redirect('http://localhost:5000/')
        return render_template('dashboard.html', doctor_id=session['doctor_id'])
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
