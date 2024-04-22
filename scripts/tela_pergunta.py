import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import random
from perguntas import lista_perguntas

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pergunta")
        self.master.geometry("400x500")
        self.style = Style(theme="flatly")
        self.score = 0

        # Configure the font size for the question and escolha buttons
        self.style.configure("TLabel", font=("Helvetica", 20))
        self.style.configure("TButton", font=("Helvetica", 16))

        # Create the question label
        self.qs_label = ttk.Label(
            self.master,
            anchor="center",
            padding=10
        )
        self.qs_label.pack(pady=10)

        # Create the escolha buttons
        self.choice_btns = []
        for i in range(3):
            button = ttk.Button(
                self.master,
                command=lambda i=i: self.verificar_resposta(i)
            )
            button.pack(pady=5, fill='x')
            self.choice_btns.append(button)

        # Create the feedback label
        self.feedback_label = ttk.Label(
            self.master,
            anchor="center",
            padding=10
        )
        self.feedback_label.pack(pady=10)
        self.mostrar_pergunta()

    def mostrar_pergunta(self):
    
        self.current_question = random.choice(lista_perguntas)
        self.qs_label.config(text=self.current_question["pergunta"])

        # Determine wraplength dynamically based on the length of the question text
        wraplength = len(self.current_question["pergunta"]) * 10
        self.qs_label.config(wraplength=wraplength)

        # Display the choices on the buttons
        escolhas = self.current_question["escolhas"]
        for i in range(3):
            self.choice_btns[i].config(text=escolhas[i], state="normal")

        # Clear the feedback label
        self.feedback_label.config(text="")

    def verificar_resposta(self, escolha):
        resposta_selecionada = self.choice_btns[escolha].cget("text")
        if resposta_selecionada == self.current_question["resposta"]:
            self.feedback_label.config(text="Correto!", foreground="green")
        else:
            self.feedback_label.config(text="Incorreto!", foreground="red")
        
        for button in self.choice_btns:
            button.config(state="disabled")

# Create the main window
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
