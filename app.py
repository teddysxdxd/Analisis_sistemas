from flask import Flask, render_template, request, jsonify, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'umg_analisis_secret' # Necesario para sesiones
# Usamos la ruta del volumen de Render que configuramos
DB_PATH = '/app/data/database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Inicialización segura
if not os.path.exists('/app/data'):
    os.makedirs('/app/data', exist_ok=True)

conn = get_db_connection()
conn.execute('''CREATE TABLE IF NOT EXISTS cosechas 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, producto TEXT, variedad TEXT, cantidad REAL, unidad TEXT, referencia TEXT)''')
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    # Validación simple: si hay texto en ambos campos, entra
    if data.get('user') and data.get('password'):
        session['user'] = data['user']
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Datos obligatorios"}), 401

@app.route('/api/cosecha', methods=['POST'])
def guardar_cosecha():
    if 'user' not in session:
        return jsonify({"status": "error", "message": "Debe iniciar sesión primero"}), 403
    
    data = request.json
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO cosechas (producto, variedad, cantidad, unidad, referencia) VALUES (?, ?, ?, ?, ?)',
                     (data['producto'], data['variedad'], data['cantidad'], data['unidad'], 'Plaza Central'))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500