import tkinter as tk
from tkinter import messagebox

class TesteManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Teste Manager")
        master.geometry("500x400")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.master, text="Gerenciador de Teste", font=("Helvetica", 20, "bold"))
        title.pack(pady=20)

        user_button = tk.Button(self.master, text="Gerenciar Usuários", width=30, command=self.user_action)
        user_button.pack(pady=10)

        product_button = tk.Button(self.master, text="Gerenciar Produtos", width=30, command=self.product_action)
        product_button.pack(pady=10)

        billing_button = tk.Button(self.master, text="Faturamento", width=30, command=self.billing_action)
        billing_button.pack(pady=10)

        exit_button = tk.Button(self.master, text="Sair", width=30, command=self.master.quit)
        exit_button.pack(pady=30)

    def user_action(self):
        messagebox.showinfo("Usuários", "Funcionalidade de usuários em construção.")

    def product_action(self):
        messagebox.showinfo("Produtos", "Funcionalidade de produtos em construção.")

    def billing_action(self):
        messagebox.showinfo("Faturamento", "Funcionalidade de faturamento em construção.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TesteManagerApp(root)
    root.mainloop()
