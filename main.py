from tkinter import *
from tkinter import Tk, ttk
from PIL import Image, ImageTk
from tkinter import messagebox

#Barra de progresso
from tkinter.ttk import Progressbar

#matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

#calendario

from tkcalendar import Calendar, DateEntry
from datetime import date

# funcoes 
from visualizando import bar_valores, pie_valores, porcentagem_valores, inserir_categoria, ver_categorias, inserir_receitas, inserir_gastos, tabela, deletar_gastos, deletar_receitas


# cores 
co0 = "#2e2d2b"  
co1 = "#feffff"  
co2 = "#4fa882" 
co3 = "#38576b"  
co4 = "#403d3d"  
co5 = "#e06636"  
co6 = "#038cfc"   
co7 = "#3fbfb9"  
co8 = "#263238"  
co9 = "#e9edf5"   

colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']

#janela
janela = Tk()
janela.title()
janela.geometry('900x650')
janela.configure(background=co9)
janela.resizable(width=FALSE, height=FALSE)

style = ttk.Style(janela)
style.theme_use("clam")

# Divisoes 
# Cima

frameCima = Frame(janela, width=1043, height=50, bg=co1, relief="flat")
frameCima.grid(row=0, column=0)

#meio

frameMeio = Frame(janela, width=1043, height=361, bg=co1, pady=20, relief="raised")
frameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

#baixo

frameBaixo = Frame(janela, width=1043, height=300, bg=co1, relief="flat")
frameBaixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

#grafico

frame_gra_pie = Frame(frameMeio, width=580, height=250, bg=co2)
frame_gra_pie.place(x=415, y=5)

#detahes cima
app_img = Image.open("logo.png")
app_img = app_img.resize((45,45))
app_img = ImageTk.PhotoImage(app_img)
app_logo= Label(frameCima, image=app_img, text="Assistente Pessoal de Finanças", width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=("verdana 20 bold"), bg=co1, fg=co4, )
app_logo.place(x=0, y=0)

#defenino tree
global tree

# função para inserir 
def inserir_categorias_b():
    nome = e_categoria.get()

    lista_inserir = [nome]
    for i in lista_inserir:
        if i=="":
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
        
    inserir_categoria(lista_inserir)  
    messagebox.showinfo("Sucesso", "Os dados foram inseridos com sucesso")  

    e_categoria.delete (0, 'end')

    categorias_funcao = ver_categorias()
    categoria = []

    for i in categorias_funcao:
        categoria.append(i[1])

     # atualizando lista    
    combo_categoria_despesas["values"] = (categoria)

#inserir receitas 

def inseirir_receitas_b():
    nome = 'Receitas'
    data = e_cal_receitas.get()
    quantia = e_valor_receitas.get()
    
    lista_inserir = [nome, data , quantia ]

    for i in lista_inserir:
        if i=="":
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
        
    inserir_receitas(lista_inserir)

    messagebox.showinfo("Sucesso", "Os dados foram inseridos com sucesso")
    e_cal_receitas.delete(0, 'end')
    e_valor_receitas.delete(0, 'end')

    # atualizar dados 

    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()

#inserir despesas  

def inseirir_despesas_b():

    nome = combo_categoria_despesas.get()
    data = e_cal_despesas.get()
    quantia = e_valor_despesas.get()
    
    lista_inserir = [nome, data , quantia ]

    for i in lista_inserir:
        if i=="":
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
        
    inserir_gastos(lista_inserir)

    messagebox.showinfo("Sucesso", "Os dados foram inseridos com sucesso")

    combo_categoria_despesas.delete(0, 'end')
    e_cal_despesas.delete(0, 'end')
    e_valor_despesas.delete(0, 'end')

    # atualizar dados 

    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()

# funcao deletar 

def deletar_dados():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor = treev_lista[0]
        nome = treev_lista[1]

        if nome == 'Receitas':
            deletar_receitas([valor])
            messagebox.showinfo("Sucesso", "Os dados foram deletados com sucesso")

        
            mostrar_renda()
            porcentagem()
            grafico_bar()
            resumo()
            grafico_pie()

        else:
            deletar_gastos([valor])
            messagebox.showinfo("Sucesso", "Os dados foram deletados com sucesso")

        
            mostrar_renda()
            porcentagem()
            grafico_bar()
            resumo()
            grafico_pie()

    except IndexError:   
        messagebox.showerror('Erro', 'Selecione um dos dados na tabela')


#porcentagem------------------

def porcentagem():
    l_nome = Label(frameMeio, text= "Porcentagem de Gastos", height=1, anchor=NW, font=("verdana 12"), bg=co1, fg=co4)
    l_nome.place(x=7, y=5)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("black.Horizontal.TProgessbar", background="#daed6b")
    style.configure("TProgressbar", thickness=25)
    barra = Progressbar(frameMeio, length=180, style="balck.Horizontal.TProgressbar")
    barra.place(x=0, y=35)
    barra['value']= porcentagem_valores()[0]

    valor = porcentagem_valores()[0]

    l_porcentagem = Label(frameMeio, text= "{:,.2f}%".format(valor), anchor=NW, font=("verdana 12"), bg=co1, fg=co4)
    l_porcentagem.place(x=200, y=35)

#Grafico

def grafico_bar():
    lista_categorias = ["Renda", "Despesas", "Saldos"]
    lista_valores = bar_valores()

    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)
    #ax.autoscale(enable=True, axis='both', tight=None)

    ax.bar(lista_categorias, lista_valores,  color=colors, width=0.9)
    #create a list to collect the plt.patches data

    c = 0
    #set individual bar lables using above list
    for i in ax.patches:
        #get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic',  verticalalignment='bottom',color='dimgrey')
        c += 1

    ax.set_xticklabels(lista_categorias,fontsize=16)

    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(False, color='#EEEEEE')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=70)

# função de resumo total
def resumo():
    valor = bar_valores()
    l_linha = Label(frameMeio, text ="", width=215, height=1,anchor=NW, font=("Arial 1"), bg="#545454")
    l_linha.place(x=309, y=52)
    l_sumario = Label(frameMeio, text ="Total da renda mensal      ".upper(),anchor=NW, font=("verdana 12"), bg=co1, fg="#83a9e6")
    l_sumario.place(x=309, y=35)
    l_sumario = Label(frameMeio, text ="R${:,.2f}".format(valor[0]),anchor=NW, font=("arial 17"), bg=co1, fg="#000000")
    l_sumario.place(x=309, y=70)

    l_linha = Label(frameMeio, text ="", width=215, height=1,anchor=NW, font=("Arial 1"), bg="#545454")
    l_linha.place(x=309, y=132)
    l_sumario = Label(frameMeio, text ="Total Despesas mensais  ".upper(),anchor=NW, font=("verdana 12"), bg=co1, fg="#83a9e6")
    l_sumario.place(x=309, y=115)
    l_sumario = Label(frameMeio, text ="R${:,.2f}".format(valor[0]),anchor=NW, font=("arial 17"), bg=co1, fg="#000000")
    l_sumario.place(x=309, y=150)

    l_linha = Label(frameMeio, text ="", width=215, height=1,anchor=NW, font=("Arial 1"), bg="#545454")
    l_linha.place(x=309, y=207)
    l_sumario = Label(frameMeio, text ="Saldo Total      ".upper(),anchor=NW, font=("verdana 12"), bg=co1, fg="#83a9e6")
    l_sumario.place(x=309, y=190)
    l_sumario = Label(frameMeio, text ="R${:,.2f}".format(valor[0]),anchor=NW, font=("arial 17"), bg=co1, fg="#000000")
    l_sumario.place(x=309, y=220)

#grafico de Pie:

def grafico_pie():
 
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figura.add_subplot(111)

    lista_valores = pie_valores()[1]
    lista_categorias = pie_valores()[0]


    explode = []
    for i in lista_categorias:
        explode.append(0.05)

    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90)
    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pie)
    canva_categoria.get_tk_widget().grid(row=0, column=0)


porcentagem()
grafico_bar()
resumo()
grafico_pie()

# divisão de baixo 

frame_renda = Frame(frameBaixo, width=300, height=250, bg=co1,)
frame_renda.grid(row=0, column=0)

frame_operacoes = Frame(frameBaixo, width=220, height=250, bg=co1,)
frame_operacoes.grid(row=0, column=1, padx=5)

frame_configuracao = Frame(frameBaixo, width=220, height=250, bg=co1,)
frame_configuracao.grid(row=0, column=2, padx=5)

#Tabela De Renda Mensal ---------------------------

app_tabela= Label(frameMeio, text="Tabela de Gastos", anchor=NW, font=("verdana 12"), bg=co1, fg=co4, )
app_tabela.place(x=5, y=309)

#Codigo tabela

def mostrar_renda():

    tabela_head = ['#Id','Categoria','Data','Valor']

    lista_itens = tabela()
    
    global tree

    tree = ttk.Treeview(frame_renda, selectmode="extended",columns=tabela_head, show="headings")
   
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)
    
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)

    
mostrar_renda()  

#configuraçoes despesas 
l_info = Label(frame_operacoes, text = "Insira novas despesas", height=1, anchor=NW, font=("Verdana 10 bold"), bg=co1, fg=co4)
l_info.place(x=10, y=10)

e_categoria = Label(frame_operacoes, text = "Categoria", height=1, anchor=NW, font=("Ivy 10"), bg=co1, fg=co4)
e_categoria.place(x=10, y=40)

categoria_funcao = ver_categorias()
categoria = []

for i in categoria_funcao:
    categoria.append(i[1])

combo_categoria_despesas = ttk.Combobox(frame_operacoes, width=10, font=("Ivy 10"), ) 
combo_categoria_despesas["values"] = (categoria)
combo_categoria_despesas.place (x=110, y = 41) 

l_cal_categoria = Label(frame_operacoes, text = "Data", height=1, anchor=NW, font=("Ivy 10"), bg=co1, fg=co4)
l_cal_categoria.place(x=10, y=70)

e_cal_despesas = DateEntry(frame_operacoes, width=12, background="darkblue", foreground="white", borderwidth=2, year=2023)
e_cal_despesas.place(x=110, y = 71)

#valor

l_valor_categoria = Label(frame_operacoes, text = "Valor Total", height=1, anchor=NW, font=("Ivy 10"), bg=co1, fg=co4)
l_valor_categoria.place(x=10, y=100)

e_valor_despesas = Entry(frame_operacoes, width=14, justify='left', relief='solid')
e_valor_despesas.place(x=110, y =101)

#Botao inserir 

img_add_despesas = Image.open("logo.png")
img_add_despesas.resize((17,17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)


botao_inserir_despesas = Button(frame_operacoes, command= inseirir_receitas_b,  image=app_img, text="Adicionar   ".upper(), width=100, compound=LEFT, anchor=NW, font=("Ivy 7 bold"), bg=co1, fg=co0, overrelief=RIDGE, )
botao_inserir_despesas.place(x=110, y=131)

#botao de deletar


img_delete = Image.open("logo.png")
img_delete.resize((17,17))
img_delete = ImageTk.PhotoImage(img_delete)

botao_delete = Button(frame_operacoes, command= deletar_dados,  image=app_img, text="Deletar   ".upper(), width=90, compound=LEFT, anchor=NW, font=("Ivy 7 bold"), bg=co1, fg=co0, overrelief=RIDGE, )
botao_delete.place(x=110, y=190)


#configuraçoes receitas

l_info = Label(frame_configuracao, text = "Insira novas Receitas", height=1, anchor=NW, font=("Verdana 10 bold"), bg=co1, fg=co4)
l_info.place(x=10, y=10)

#calendario
l_cal_receitas = Label(frame_configuracao, text = "Data", height=1, anchor=NW, font=("Ivy 10"), bg=co1, fg=co4)
l_cal_receitas.place(x=10, y=40)
e_cal_receitas = DateEntry(frame_configuracao, width=12, background="darkblue", foreground="white", borderwidth=2, year=2023)
e_cal_receitas.place(x=110, y = 41)

#valor
l_valor_receitas = Label(frame_configuracao, text = "Valor Total", height=1, anchor=NW, font=("Ivy 10"), bg=co1, fg=co4)
l_valor_receitas.place(x=10, y=70)
e_valor_receitas = Entry(frame_configuracao, width=14, justify='left', relief='solid')
e_valor_receitas.place(x=110, y = 71)

#botao

img_receitas = Image.open("logo.png")
img_receitas.resize((17,17))
img_receitas = ImageTk.PhotoImage(img_receitas)

botao_add = Button(frame_configuracao, command= inseirir_receitas_b, image=app_img, text="Adicionar   ".upper(), width=100, compound=LEFT, anchor=NW, font=("Ivy 7 bold"), bg=co1, fg=co0, overrelief=RIDGE, )
botao_add.place(x=110, y=111)

#configuraçoes categorias

l_info = Label(frame_configuracao, text = "Categoria", height=1, anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4)
l_info.place(x=10, y=170)

e_categoria = Entry(frame_configuracao, width=14, justify='left', relief='solid')
e_categoria.place(x=110, y = 170)

#botao

img_categoria = Image.open("logo.png")
img_categoria.resize((17,17))
img_categoria = ImageTk.PhotoImage(img_categoria)

botao_categoria = Button(frame_configuracao,command=inserir_categorias_b, image=app_img, text="Adicionar   ".upper(), width=100, compound=LEFT, anchor=NW, font=("Ivy 7 bold"), bg=co1, fg=co0, overrelief=RIDGE, )
botao_categoria.place(x=110, y=190)



janela.mainloop()
