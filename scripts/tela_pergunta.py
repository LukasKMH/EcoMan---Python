import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import textwrap
import random
from perguntas import lista_perguntas

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pergunta")
        self.root.geometry("500x500")
        self.style = Style(theme="flatly")

        # Configure the font size for the question and escolha buttons
        self.style.configure("TLabel", font=("Helvetica", 18))
        self.style.configure("TButton", font=("Helvetica", 12), background='#eab676', foreground='#000000')  # Definindo a cor de fundo dos botões

        # Create the question label
        self.titulo_pergunta = ttk.Label(
            self.root,
            anchor="center",
            padding=10,
            justify="center"  # Adicionando justificação centralizada
        )
        self.titulo_pergunta.pack(pady=10)

        # Create the escolha buttons
        self.choice_btns = []
        for i in range(3):
            button = ttk.Button(
                self.root,
                command=lambda i=i: self.verificar_resposta(i),
            )
            button.pack(pady=(20, 0), padx=20, fill='x')  # Adiciona margem superior de 5 pixels e margem inferior de 0 pixels
            self.choice_btns.append(button)

        # Create the feedback label
        self.feedback_label = ttk.Label(
            self.root,
            anchor="center",
            padding=10
        )
        self.feedback_label.pack(pady=10)
        self.mostrar_pergunta()

    def mostrar_pergunta(self):
        self.pergunta_atual = random.choice(lista_perguntas)
        self.titulo_pergunta.config(text=self.pergunta_atual["pergunta"])
        self.titulo_pergunta.config(wraplength=380)

        # Display the choices on the buttons
        escolhas = self.pergunta_atual["escolhas"]
        for i in range(3):
            self.choice_btns[i].config(text=escolhas[i], state="normal")
            self.ajustar_texto_botao(self.choice_btns[i], escolhas[i])  # Chame a função para ajustar o texto do botão

        # Clear the feedback label
        self.feedback_label.config(text="")

    def verificar_resposta(self, escolha):
        resposta_selecionada = self.choice_btns[escolha].cget("text")
        if resposta_selecionada == self.pergunta_atual["resposta"]:
            self.feedback_label.config(text="Correto!", foreground="green")
        else:
            self.feedback_label.config(text="Incorreto!", foreground="red")
        
        for button in self.choice_btns:
            button.config(state="disabled")

    def ajustar_texto_botao(self, button, texto):
        max_width = 44  # Defina o número máximo de caracteres por linha
        if len(texto) > max_width:
            texto_quebrado = textwrap.fill(texto, max_width)
            button.config(text=texto_quebrado)


# Create the main window
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
