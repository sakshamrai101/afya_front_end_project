from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Initialize database connection
def get_db_connection():
    conn = sqlite3.connect('patient_info.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

# Initialize the database tables
def init_db():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                gender TEXT,
                dob DATE,
                phone TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                zip_code TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS guardians (
                id INTEGER PRIMARY KEY,
                patient_id INTEGER,
                first_name TEXT,
                last_name TEXT,
                relationship TEXT,
                other_specify TEXT,
                phone_belong TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(id)
            )
        ''')
        conn.commit()

@app.route('/')
def basic_info():
    return render_template('basic_info.html')

@app.route('/guardian_info')
def guardian_info():
    return render_template('guardian_info.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation_template.html')

@app.route('/consent')
def show_consent():
    return render_template('consent.html')

@app.route('/submit')
def submission():
    return render_template('submit.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.get_json()
    conn = get_db_connection()
    c = conn.cursor()

    # Insert patient information
    c.execute('''
        INSERT INTO patients (first_name, last_name, gender, dob, phone, address, city, state, zip_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['firstName'], data['lastName'], data['gender'], data['dob'], data['phone'], data['address'], data['city'], data['state'], data['zip']))

    patient_id = c.lastrowid # primary key

    # Insert guardian information if it exists
    guardian = data.get('guardianInfo') 
    if guardian:
        c.execute('''
            INSERT INTO guardians (patient_id, first_name, last_name, relationship, other_specify, phone_belong)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (patient_id, guardian['firstName'], guardian['lastName'], guardian['relationship'], guardian.get('otherSpecify', ''), guardian['phoneBelong']))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Data saved successfully', 'patient_id': patient_id}), 200

# Ensure the DB is initialized when running the app
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)
