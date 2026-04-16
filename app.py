from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'data/database.db'

# Asegurar que la carpeta data exista para el volumen de Docker
if not os.path.exists('data'):
    os.makedirs('data')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Tabla de Cosechas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cosechas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            variedad TEXT,
            cantidad REAL,
            unidad TEXT,
            referencia TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cosecha', methods=['POST'])
def guardar_cosecha():
    data = request.json
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cosechas (producto, variedad, cantidad, unidad, referencia)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['producto'], data['variedad'], data['cantidad'], data['unidad'], data['referencia']))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Cosecha registrada"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)