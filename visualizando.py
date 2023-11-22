import sqlite3 as lite
import pandas as pd

#Conexão 
conexao = lite.connect("dados.db")

#Funcoes para inserir dados--------------------------------------
#Inserindo categorias 

def inserir_categoria(i):
    with conexao:
        x = conexao.cursor()
        query = "insert into categorias(nome) VALUES (?)"
        conexao.execute(query, i)


#Inserindo receitas 

def inserir_receitas(i):
    with conexao:
        x = conexao.cursor()
        query = "insert into receitas(categoria, adicionado_em, valor) VALUES (?,?,?)"
        conexao.execute(query, i)

#Inserindo gastos 

def inserir_gastos(i):
    with conexao:
        x = conexao.cursor()
        query = "insert into receitas(categoria, retirado_em, valor) VALUES (?,?,?)"
        conexao.execute(query, i)


#Funcoes para deletar -----------------------------------------------------

#Deletar receitas
def deletar_receitas(i):
    with conexao:
        x = conexao.cursor()
        query = "DELETE FROM receitas WHERE id=?"
        x.execute(query, i)

#Deletar gastos
def deletar_gastos(i):
    with conexao:
        x = conexao.cursor()
        query = "DELETE FROM gastos WHERE id=?"
        x.execute(query, i)

# Funcoes para ver dados ---------------------------------------------

#ver categoria
def ver_categorias():

    lista_itens = []

    with conexao:
        x = conexao.cursor()
        conexao.execute("SELECT * FROM categorias")
        linha = x.fetchall()
        for i in linha:
            lista_itens.append(1)

    return lista_itens
print(ver_categorias())

#ver receitas
def ver_receitas():

    lista_itens = []

    with conexao:
        x = conexao.cursor()
        conexao.execute("SELECT * FROM receitas")
        linha = x.fetchall()
        for i in linha:
            lista_itens.append(1)

    return lista_itens

#ver gastos
def ver_gastos():

    lista_itens = []

    with conexao:
        x = conexao.cursor()
        conexao.execute("SELECT * FROM gastos")
        linha = x.fetchall()
        for i in linha:
            lista_itens.append(1)

    return lista_itens

#funcoes para dados da tabela 
def tabela():
    gastos = ver_gastos()
    receitas = ver_receitas()

    tabela_lista =[]

    for i in gastos:
        tabela_lista.append(i)

    for i in receitas:
        tabela_lista.append(i) 

    return tabela_lista

# funcao para grafico 

def bar_valores():

    receitas = ver_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])        
    
    receita_total = sum(receitas_lista)

    #despesas total

    gastos = ver_gastos()
    gastos_lista = []
 
    for i in gastos:
        gastos_lista.append(i[3])        
    
    gasto_total = sum(gastos_lista)  

    # saldo total 
    saldo_total = receita_total - gasto_total

    return [receita_total, gasto_total, saldo_total ]

#função grafico pie
def pie_valores():
    gastos = ver_gastos()
    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    dataframe =  pd.DataFrame(tabela_lista, columns= ['id','categoria', 'Data', 'valor'])  
    datafreme = dataframe.groupby('categoria')['valor'].sum()

    lista_quantias = dataframe.values.tolist()  
    lista_categorias = []

    for i in datafreme.index:
        lista_categorias.append(i)

    return ([lista_categorias, lista_quantias])  

#funcao porcentagem  

def porcentagem_valores():

    receitas = ver_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])        
    
    receita_total = sum(receitas_lista)

    #despesas total

    gastos = ver_gastos()
    gastos_lista = []
 
    for i in gastos:
        gastos_lista.append(i[3])        
    
    gasto_total = sum(gastos_lista)  

    # porcetagem total 
    if gasto_total <= 0:
        total = 0
    else:
        total=((receita_total-gasto_total)/ receita_total)*100
        

    return [total]