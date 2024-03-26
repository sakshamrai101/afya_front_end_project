from flask import Flask, request, jsonify, send_from_directory, redirect
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def serve_form():
    return send_from_directory(os.getcwd(), 'basic_info.html')

def init_db():
    conn = sqlite3.connect('patient_info.db')
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
    conn.close()

init_db()

@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.form
    conn = sqlite3.connect('patient_info.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO patients (first_name, last_name, gender, dob, phone, address, city, state, zip_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['firstName'], data['lastName'], data['gender'], f"{data['year']}-{data['month']}-{data['day']}", data['phone'], data['address'], data['city'], data['state'], data['zip']))
    conn.commit()
    patient_id = c.lastrowid
    conn.close()
    return jsonify({'patient_id': patient_id}), 200

@app.route('/submit-guardian-form', methods=['POST'])
def submit_guardian_form():
    data = request.form
    conn = sqlite3.connect('patient_info.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO guardians (patient_id, first_name, last_name, relationship, other_specify, phone_belong)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['patient_id'], data['firstName'], data['lastName'], data['relationship'], data['other-specify'], data['phone-belong']))
    conn.commit()
    conn.close()
    return redirect('/confirmation.html')

#@app.route('/guardian-info')
#def guardian_info():
#    return send_from_directory(os.getcwd(), 'guardian_info.html')

#@app.route('/confirmation.html')
#def confirmation():
 #   return send_from_directory(os.getcwd(), 'confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
