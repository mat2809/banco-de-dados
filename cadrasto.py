import sqlite3
import tkinter as tk
from tkinter import messagebox

# Conexão com banco SQLite
conn = sqlite3.connect('cadastro.db')
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pessoas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')
conn.commit()

# Função para salvar cadastro
def salvar():
    nome = entry_nome.get()
    email = entry_email.get()
    
    if nome == "" or email == "":
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
        return

    cursor.execute("INSERT INTO pessoas (nome, email) VALUES (?, ?)", (nome, email))
    conn.commit()
    messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")

    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    
    atualizar_lista()

# Função para carregar usuários na lista
def atualizar_lista():
    listbox_usuarios.delete(0, tk.END)
    cursor.execute("SELECT nome, email FROM pessoas ORDER BY id DESC")
    for nome, email in cursor.fetchall():
        listbox_usuarios.insert(tk.END, f"{nome} - {email}")

# Interface gráfica
janela = tk.Tk()
janela.title("Cadastro de Pessoas")
janela.geometry("400x400")

# Formulário
tk.Label(janela, text="Nome:").pack(pady=5)
entry_nome = tk.Entry(janela, width=40)
entry_nome.pack()

tk.Label(janela, text="Email:").pack(pady=5)
entry_email = tk.Entry(janela, width=40)
entry_email.pack()

btn_salvar = tk.Button(janela, text="Salvar", command=salvar)
btn_salvar.pack(pady=10)

# Lista de usuários
tk.Label(janela, text="Usuários cadastrados:").pack(pady=5)
listbox_usuarios = tk.Listbox(janela, width=50, height=10)
listbox_usuarios.pack(pady=5)

# Carregar usuários ao iniciar
atualizar_lista()

# Rodar interface
janela.mainloop()

# Encerrar conexão (opcional)
conn.close()
