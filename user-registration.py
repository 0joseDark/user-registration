from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def is_strong_password(password):
    # Verifica se a senha tem pelo menos 8 caracteres, uma letra maiúscula,
    # uma letra minúscula, um dígito e um caractere especial
    if (len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
        return True
    return False

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Nome de utilizador e senha são obrigatórios"}), 400
    
    if not is_strong_password(password):
        return jsonify({"error": "A senha não é forte o suficiente"}), 400
    
    # Aqui pode adicionar código para guardar o novo utilizador na base de dados
    
    return jsonify({"message": "Utilizador registado com sucesso"}), 201

if __name__ == '__main__':
    app.run(debug=True)
