import sqlite3 as lite

#Conexão 
conexao = lite.connect("dados.db")

#Categorias 
with conexao:
    x = conexao.cursor()
    x.execute("CREATE TABLE categorias(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)")

#RECEITAS 
with conexao:
    x = conexao.cursor()
    x.execute("CREATE TABLE receitas(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor DECIMAL)")

#GASTOS
with conexao:
    x = conexao.cursor()
    x.execute("CREATE TABLE gastos(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor DECIMAL)")
