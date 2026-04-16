import os
from flask import Flask, render_template, request, jsonify, session

# Configuramos la carpeta de templates para que apunte a la raíz del proyecto
app = Flask(__name__, template_folder='../templates')
app.secret_key = 'umg_analisis_sistema_key'

@app.route('/')
def index():
    # Renderiza el archivo que tienes en /templates/index.html
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    # Validación simple para el prototipo según el DERCAS [cite: 28]
    if data.get('user') and data.get('password'):
        session['user'] = data['user']
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Credenciales inválidas"}), 401

@app.route('/api/cosecha', methods=['POST'])
def guardar_cosecha():
    # En Vercel no podemos usar SQLite local, así que solo validamos
    # la recepción de datos para que el frontend no dé error 500
    if 'user' not in session:
        return jsonify({"status": "error", "message": "No autorizado"}), 403
    
    data = request.json
    if data:
        # Simulamos éxito para el prototipo funcional [cite: 41]
        return jsonify({"status": "success", "message": "Datos recibidos en el servidor"}), 201
    return jsonify({"status": "error", "message": "Datos incompletos"}), 400

# Esta parte es CRÍTICA para que Vercel reconozca la función Serverless
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)