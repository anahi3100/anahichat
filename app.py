from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_anahi'
socketio = SocketIO(app, cors_allowed_origins="*")

# Diccionario de emojis
emojis = {
    ":)": "😊", ":(": "😞", ":D": "😃", ":P": "😛",
    "<3": "❤️", ":/": "😕", ";)": "😉", ":*": "😘",
    "lol": "😂", "fire": "🔥", "like": "👍", "star": "⭐"
}

usuarios_conectados = {}

def convertir_emojis(texto):
    for atajo, emoji in emojis.items():
        texto = texto.replace(atajo, emoji)
    return texto

@socketio.on('connect')
def handle_connect():
    print('Alguien se conectó')

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in usuarios_conectados:
        usuario = usuarios_conectados[request.sid]
        del usuarios_conectados[request.sid]
        emit('mensaje_chat', {'mensaje': f'**{usuario} se desconectó**', 'tipo': 'sistema'}, broadcast=True)

@socketio.on('registrar_usuario')
def registrar_usuario(data):
    usuario = data['usuario']
    usuarios_conectados[request.sid] = usuario
    emit('mensaje_chat', {'mensaje': f'**{usuario} se conectó**', 'tipo': 'sistema'}, broadcast=True)

@socketio.on('mensaje_chat')
def handle_mensaje(data):
    if request.sid in usuarios_conectados:
        usuario = usuarios_conectados[request.sid]
        mensaje = convertir_emojis(data['mensaje'])
        emit('mensaje_chat', {'mensaje': f'{usuario}: {mensaje}', 'tipo': 'usuario'}, broadcast=True)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)