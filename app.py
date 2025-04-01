
from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageFilter
import io
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'secretkey'  # Alterar para algo mais seguro
login_manager = LoginManager()
login_manager.init_app(app)

# Definindo um usuário simples
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Banco de dados fictício de usuários
users = {'admin': {'password': '1234'}}  # Definir nome de usuário e senha

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Funções de manipulação da imagem
def apply_blur(image):
    return image.filter(ImageFilter.BLUR)

def apply_sharpening(image):
    return image.filter(ImageFilter.SHARPEN)

def rotate_image(image):
    return image.rotate(45)

# Rota para login
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username in users and users[username]['password'] == password:
        user = User(username)
        login_user(user)
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Rota para carregar e manipular a imagem
@app.route('/process_image', methods=['POST'])
@login_required
def process_image():
    img_file = request.files.get('image')
    if not img_file:
        return jsonify({"message": "No image provided!"}), 400
    
    img = Image.open(img_file)
    
    # Verificando qual operação será feita
    action = request.form.get('action')
    
    if action == 'blur':
        img = apply_blur(img)
    elif action == 'sharpen':
        img = apply_sharpening(img)
    elif action == 'rotate':
        img = rotate_image(img)
    else:
        return jsonify({"message": "Invalid action!"}), 400

    # Convertendo a imagem para enviar como resposta
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
