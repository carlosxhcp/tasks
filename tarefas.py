import customtkinter as ctk
import json
import os
import requests
from io import BytesIO
from PIL import Image


# Parte que utilizei uma função para carregar as imagens externamente
URL_DELETAR = "https://i.ibb.co/LBwY8x1/deletar.png"
URL_CONCLUIDO = "https://i.ibb.co/Zz4z5hzD/concluido.png"
def carregar_img(url):
    return Image.open(BytesIO(requests.get(url).content))
icon_deletar = ctk.CTkImage(dark_image=carregar_img(URL_DELETAR))
icon_concluido = ctk.CTkImage(dark_image=carregar_img(URL_CONCLUIDO))


# Abrindo o arquivo que armazena as tarefas
TAREFAS_JSON = "tarefas.json"

# Configuração da janela principal
ctk.set_appearance_mode("dark")
janela = ctk.CTk()
janela.title("Minhas Tarefas")
janela.geometry("500x500")

# Função para salvar as tarefas no arquivo JSON
def salvar_tarefas():
    tarefas = []
    for widget in lista_tarefas.winfo_children():
        if isinstance(widget, ctk.CTkFrame):
            texto_label = widget.winfo_children()[0]
            concluida = "✔" in texto_label.cget("text")
            tarefa_texto = texto_label.cget("text").replace(" ✔", "")
            tarefas.append({"texto": tarefa_texto, "concluida": concluida})
    
    with open(TAREFAS_JSON, 'w') as f:
        json.dump(tarefas, f)

# Função para carregar tarefas do arquivo JSON
def carregar_tarefas():
    if os.path.exists(TAREFAS_JSON):
        with open(TAREFAS_JSON, 'r') as f:
            try:
                tarefas = json.load(f)
                for tarefa in tarefas:
                    add_item_tarefa(tarefa["texto"], tarefa["concluida"])
            except json.JSONDecodeError:
                pass

# Função para adicionar nova tarefa
def add_tarefa():
    tarefa = entrada.get().strip()
    if tarefa:
        add_item_tarefa(tarefa, False)
        entrada.delete(0, ctk.END)
        salvar_tarefas()

# Função para adicionar item à lista
def add_item_tarefa(tarefa, concluida):
    item = ctk.CTkFrame(lista_tarefas, fg_color="#2B2B2B")
    item.pack(fill="x", pady=2, padx=5)

    texto = ctk.CTkLabel(item, text=tarefa + (" ✔" if concluida else ""), fg_color="#2B2B2B", anchor="w", font=('Arial', 20))
    texto.pack(side="left", fill="x", expand=True, padx=5)

    frame_botoes = ctk.CTkFrame(item)
    frame_botoes.pack(side="right", padx=5)

    btn_check = ctk.CTkButton(frame_botoes, text="", image=icon_concluido, fg_color="#2B2B2B", hover_color="#3D3D3D", width=25, command=lambda: marcar_concluido(texto))
    btn_check.pack(side="left", padx=2)

    btn_remover = ctk.CTkButton( frame_botoes, text="", image=icon_deletar, width=25, fg_color="#2B2B2B", hover_color="#3D3D3D", command=lambda: remover_tarefa(item))
    btn_remover.pack(side="left", padx=2)

# Função para remover tarefa
def remover_tarefa(item):
    item.destroy()
    salvar_tarefas()

# Função para marcar tarefa como concluída
def marcar_concluido(label):
    texto = label.cget("text")
    if "✔" in texto:
        label.configure(text=texto.replace(" ✔", ""))
    else:
        label.configure(text=texto + " ✔")
    salvar_tarefas()

# Campo de entrada e botão adicionar
entrada = ctk.CTkEntry(janela, width=350, height=40 ,placeholder_text="Digite a tarefa")
entrada.pack(pady=10)

btn_add = ctk.CTkButton(janela, text="Adicionar",font=("Arial", 15),width=350, command=add_tarefa)
btn_add.pack(pady=5)

# Área da lista de tarefas com rolagem
frame_scroll = ctk.CTkFrame(janela)
frame_scroll.pack(fill="both", expand=True, pady=10, padx=5)

canvas = ctk.CTkCanvas(frame_scroll, width=380, height=350, background="#2B2B2B", highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ctk.CTkScrollbar(frame_scroll, command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
lista_tarefas = ctk.CTkFrame(canvas)
canvas.create_window((0, 0), window=lista_tarefas, anchor="nw")

lista_tarefas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Carregar tarefas ao iniciar
carregar_tarefas()

janela.mainloop()
