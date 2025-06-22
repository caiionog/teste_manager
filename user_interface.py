import tkinter as tk
from tkinter import ttk, messagebox
from database import *
from ttkthemes import ThemedTk

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Login - Sistema de Gerenciameimport tkinter as tk
from tkinter import ttk, messagebox
from database import *
from ttkthemes import ThemedTk, ThemedToplevel

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Login - Sistema de Gerenciamento")
        self.on_login_success = on_login_success
        
        # Centralizar a janela
        window_width = 300
        window_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Frame principal
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Widgets
        ttk.Label(self.frame, text="Usuário:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(self.frame, text="Senha:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        self.login_button = ttk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Configurar expansão das colunas
        self.frame.columnconfigure(1, weight=1)
        
        # Bind Enter key to login
        self.root.bind("<Return>", lambda event: self.login())
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos")
            return
        
        conn = create_connection()
        if conn is not None:
            user = login_user(conn, username, password)
            conn.close()
            
            if user:
                self.root.destroy()
                self.on_login_success(user)
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos")

class UserManagementApp:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("Gerenciamento de Usuários")
        
        # Configurar tamanho e centralizar
        self.root.state("zoomed")  # Maximiza a janela
        
        # Verificar se o usuário atual é admin
        self.is_admin = bool(current_user[5])  # is_admin está na posição 5
        
        # Criar widgets
        self.create_widgets()
        
        # Carregar dados
        self.load_users()
        
    def create_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Barra de ferramentas
        self.toolbar_frame = ttk.Frame(self.main_frame)
        self.toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.add_button = ttk.Button(self.toolbar_frame, text="Adicionar Usuário", command=self.show_add_user_dialog)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.edit_button = ttk.Button(self.toolbar_frame, text="Editar Usuário", command=self.show_edit_user_dialog)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(self.toolbar_frame, text="Excluir Usuário", command=self.delete_user)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.refresh_button = ttk.Button(self.toolbar_frame, text="Atualizar", command=self.load_users)
        self.refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Treeview para exibir usuários
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Username", "Full Name", "Email", "Admin"), show="headings")
        
        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Username", text="Usuário")
        self.tree.heading("Full Name", text="Nome Completo")
        self.tree.heading("Email", text="E-mail")
        self.tree.heading("Admin", text="Admin")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Username", width=150)
        self.tree.column("Full Name", width=200)
        self.tree.column("Email", width=200)
        self.tree.column("Admin", width=80, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Barra de status
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_frame, text=f"Logado como: {self.current_user[3]} ({\'Admin\' if self.is_admin else \'Usuário\'}) ")
        self.status_label.pack(side=tk.LEFT)
        
        # Desabilitar botões se não for admin
        if not self.is_admin:
            self.add_button.config(state=tk.DISABLED)
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
    
    def load_users(self):
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Carregar usuários do banco de dados
        conn = create_connection()
        if conn is not None:
            users = get_all_users(conn)
            conn.close()
            
            for user in users:
                self.tree.insert("", tk.END, values=(
                    user[0],  # ID
                    user[1],  # Username
                    user[3],  # Full Name
                    user[4],  # Email
                    "Sim" if user[5] else "Não"  # Admin
                ))
    
    def show_add_user_dialog(self):
        dialog = ThemedToplevel(self.root) # Use ThemedToplevel para a janela de diálogo
        dialog.set_theme("black") # Define o tema escuro para a janela de diálogo
        dialog.title("Adicionar Novo Usuário")
        
        # Centralizar a janela
        window_width = 400
        window_height = 300
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Frame principal
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Widgets
        ttk.Label(frame, text="Usuário:").grid(row=0, column=0, sticky=tk.W, pady=5)
        username_entry = ttk.Entry(frame)
        username_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(frame, text="Senha:").grid(row=1, column=0, sticky=tk.W, pady=5)
        password_entry = ttk.Entry(frame, show="*")
        password_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(frame, text="Nome Completo:").grid(row=2, column=0, sticky=tk.W, pady=5)
        full_name_entry = ttk.Entry(frame)
        full_name_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(frame, text="E-mail:").grid(row=3, column=0, sticky=tk.W, pady=5)
        email_entry = ttk.Entry(frame)
        email_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)
        
        is_admin_var = tk.IntVar()
        is_admin_check = ttk.Checkbutton(frame, text="Administrador", variable=is_admin_var)
        is_admin_check.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Salvar", command=lambda: self.add_user(
            dialog,
            username_entry.get(),
            password_entry.get(),
            full_name_entry.get(),
            email_entry.get(),
            is_admin_var.get()
        )).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Configurar expansão das colunas
        frame.columnconfigure(1, weight=1)
    
    def add_user(self, dialog, username, password, full_name, email, is_admin):
        if not username or not password or not full_name:
            messagebox.showerror("Erro", "Por favor, preencha pelo menos usuário, senha e nome completo")
            return
        
        conn = create_connection()
        if conn is not None:
            user_id = add_user(conn, username, password, full_name, email, is_admin)
            conn.close()
            
            if user_id:
                messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
                dialog.destroy()
                self.load_users()
            else:
                messagebox.showerror("Erro", "Não foi possível adicionar o usuário. O nome de usuário pode já estar em uso.")
    
    def show_edit_user_dialog(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione um usuário para editar")
            return
        
        user_id = self.tree.item(selected_item[0], "values")[0]
        
        conn = create_connection()
        if conn is not None:
            user = get_user_by_id(conn, user_id)
            conn.close()
            
            if user:
                dialog = ThemedToplevel(self.root) # Use ThemedToplevel para a janela de diálogo
                dialog.set_theme("black") # Define o tema escuro para a janela de diálogo
                dialog.title("Editar Usuário")
                
                # Centralizar a janela
                window_width = 400
                window_height = 300
                screen_width = dialog.winfo_screenwidth()
                screen_height = dialog.winfo_screenheight()
                x = (screen_width - window_width) // 2
                y = (screen_height - window_height) // 2
                dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
                
                # Frame principal
                frame = ttk.Frame(dialog, padding="10")
                frame.pack(fill=tk.BOTH, expand=True)
                
                # Widgets
                ttk.Label(frame, text="Usuário:").grid(row=0, column=0, sticky=tk.W, pady=5)
                username_entry = ttk.Entry(frame)
                username_entry.insert(0, user[1])
                username_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
                
                ttk.Label(frame, text="Senha (deixe em branco para manter):").grid(row=1, column=0, sticky=tk.W, pady=5)
                password_entry = ttk.Entry(frame, show="*")
                password_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
                
                ttk.Label(frame, text="Nome Completo:").grid(row=2, column=0, sticky=tk.W, pady=5)
                full_name_entry = ttk.Entry(frame)
                full_name_entry.insert(0, user[3])
                full_name_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)
                
                ttk.Label(frame, text="E-mail:").grid(row=3, column=0, sticky=tk.W, pady=5)
                email_entry = ttk.Entry(frame)
                email_entry.insert(0, user[4])
                email_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)
                
                is_admin_var = tk.IntVar(value=user[5])
                is_admin_check = ttk.Checkbutton(frame, text="Administrador", variable=is_admin_var)
                is_admin_check.grid(row=4, column=1, sticky=tk.W, pady=5)
                
                button_frame = ttk.Frame(frame)
                button_frame.grid(row=5, column=0, columnspan=2, pady=10)
                
                ttk.Button(button_frame, text="Salvar", command=lambda: self.update_user(
                    dialog,
                    user[0],
                    username_entry.get(),
                    password_entry.get() or user[2],  # Mantém a senha atual se não for alterada
                    full_name_entry.get(),
                    email_entry.get(),
                    is_admin_var.get()
                )).pack(side=tk.LEFT, padx=5)
                
                ttk.Button(button_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
                
                # Configurar expansão das colunas
                frame.columnconfigure(1, weight=1)
    
    def update_user(self, dialog, user_id, username, password, full_name, email, is_admin):
        if not username or not full_name:
            messagebox.showerror("Erro", "Por favor, preencha pelo menos usuário e nome completo")
            return
        
        conn = create_connection()
        if conn is not None:
            success = update_user(conn, user_id, username, password, full_name, email, is_admin)
            conn.close()
            
            if success:
                messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
                dialog.destroy()
                self.load_users()
            else:
                messagebox.showerror("Erro", "Não foi possível atualizar o usuário. O nome de usuário pode já estar em uso.")
    
    def delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione um usuário para excluir")
            return
        
        user_id = self.tree.item(selected_item[0], "values")[0]
        username = self.tree.item(selected_item[0], "values")[1]
        
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o usuário \'{username}\'?"):
            conn = create_connection()
            if conn is not None:
                success = delete_user(conn, user_id)
                conn.close()
                
                if success:
                    messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                    self.load_users()
                else:
                    messagebox.showerror("Erro", "Não foi possível excluir o usuário"))