from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import re
import os
from threading import Thread
import tkinter as tk
from tkinter import messagebox

app = Flask(__name__)

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
