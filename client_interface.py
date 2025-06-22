import tkinter as tk
from tkinter import ttk, messagebox
from database import *

class ClientManagementApp:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("Gerenciamento de Clientes")
        self.root.state("zoomed")

        self.create_widgets()
        self.load_clients()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(main_frame, text="Gerenciamento de Clientes", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Frame para cadastro de clientes
        input_frame = ttk.LabelFrame(main_frame, text="Cadastrar Novo Cliente", padding="10")
        input_frame.pack(fill=tk.X, pady=10)

        ttk.Label(input_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_entry = ttk.Entry(input_frame, width=40)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(input_frame, text="CPF/CNPJ:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.doc_entry = ttk.Entry(input_frame, width=40)
        self.doc_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(input_frame, text="Telefone:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.phone_entry = ttk.Entry(input_frame, width=40)
        self.phone_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(input_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.email_entry = ttk.Entry(input_frame, width=40)
        self.email_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Button(input_frame, text="Adicionar Cliente", command=self.add_new_client).grid(row=4, column=0, columnspan=2, pady=10)

        # Treeview para exibir os clientes
        ttk.Label(main_frame, text="Clientes Cadastrados", font=("Helvetica", 12, "bold")).pack(pady=10)
        self.clients_tree = ttk.Treeview(main_frame, columns=("ID", "Nome", "CPF/CNPJ", "Telefone", "Email"), show="headings")
        self.clients_tree.heading("ID", text="ID")
        self.clients_tree.heading("Nome", text="Nome")
        self.clients_tree.heading("CPF/CNPJ", text="CPF/CNPJ")
        self.clients_tree.heading("Telefone", text="Telefone")
        self.clients_tree.heading("Email", text="Email")

        self.clients_tree.column("ID", width=50, anchor=tk.CENTER)
        self.clients_tree.column("Nome", width=150)
        self.clients_tree.column("CPF/CNPJ", width=100)
        self.clients_tree.column("Telefone", width=100)
        self.clients_tree.column("Email", width=150)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.clients_tree.yview)
        self.clients_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.clients_tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def add_new_client(self):
        name = self.name_entry.get().strip()
        doc = self.doc_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        if not name or not doc:
            messagebox.showwarning("Aviso", "Nome e CPF/CNPJ são campos obrigatórios.")
            return

        conn = create_connection()
        if conn is not None:
            client_id = add_client(conn, name, doc, phone, email)
            conn.close()
            if client_id:
                messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
                self.name_entry.delete(0, tk.END)
                self.doc_entry.delete(0, tk.END)
                self.phone_entry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)
                self.load_clients()
            else:
                messagebox.showerror("Erro", "Não foi possível adicionar o cliente. Verifique se o CPF/CNPJ já existe.")

    def load_clients(self):
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)

        conn = create_connection()
        if conn is not None:
            clients = get_all_clients(conn)
            conn.close()
            for client in clients:
                self.clients_tree.insert("", tk.END, values=client)

