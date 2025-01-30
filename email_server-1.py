from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import re
import os
from threading import Thread
import tkinter as tk
from tkinter import messagebox

# Instalação dos módulos necessários no Windows 10:
# Abra o Prompt de Comando e execute:
# python -m pip install flask
# Nenhuma instalação necessária para sqlite3, re, os, threading, tkinter (módulos padrão do Python)

app = Flask(__name__)
app.secret_key = 'chave_secreta'

# Criar a base de dados para armazenar utilizadores e e-mails
def init_db():
    conn = sqlite3.connect('email_server.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            subject TEXT,
            body TEXT,
            status TEXT CHECK(status IN ('inbox', 'sent', 'draft', 'spam', 'trash'))
        )
    ''')
    conn.commit()
    conn.close()

# Função para validar e-mail
def validar_email(email):
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password or not email:
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400
    
    if not validar_email(email):
        return jsonify({"error": "E-mail inválido"}), 400
    
    conn = sqlite3.connect('email_server.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                       (username, password, email))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Nome de utilizador ou e-mail já existem"}), 400
    finally:
        conn.close()
    
    return jsonify({"message": "Utilizador registado com sucesso"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect('email_server.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        session['user'] = username
        return jsonify({"message": "Login bem-sucedido"}), 200
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/send_email', methods=['POST'])
def send_email():
    if 'user' not in session:
        return jsonify({"error": "Não autenticado"}), 401
    
    data = request.json
    sender = session['user']
    receiver = data.get('receiver')
    subject = data.get('subject', '')
    body = data.get('body', '')
    
    conn = sqlite3.connect('email_server.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO emails (sender, receiver, subject, body, status) VALUES (?, ?, ?, ?, ?)',
                   (sender, receiver, subject, body, 'sent'))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "E-mail enviado com sucesso"}), 201

@app.route('/inbox')
def inbox():
    if 'user' not in session:
        return jsonify({"error": "Não autenticado"}), 401
    
    user = session['user']
    conn = sqlite3.connect('email_server.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM emails WHERE receiver = ? AND status = "inbox"', (user,))
    emails = cursor.fetchall()
    conn.close()
    
    return jsonify(emails)

# Interface gráfica do servidor
def iniciar_interface():
    def ligar_servidor():
        Thread(target=app.run, kwargs={'debug': True, 'use_reloader': False}).start()
        messagebox.showinfo("Servidor", "Servidor iniciado com sucesso!")
    
    def desligar_servidor():
        os._exit(0)
    
    root = tk.Tk()
    root.title("Servidor de E-mail")
    root.geometry("300x200")
    
    btn_ligar = tk.Button(root, text="Ligar Servidor", command=ligar_servidor)
    btn_ligar.pack(pady=10)
    
    btn_desligar = tk.Button(root, text="Desligar", command=desligar_servidor)
    btn_desligar.pack(pady=10)
    
    btn_sair = tk.Button(root, text="Sair", command=root.quit)
    btn_sair.pack(pady=10)
    
    root.mainloop()

if __name__ == '__main__':
    init_db()
    iniciar_interface()
