import tkinter as tk
from tkinter import ttk
from user_interface import UserManagementApp
from product_interface import ProductManagementApp
from billing_interface import BillingSystem
from sales_interface import SalesManagementApp
from client_interface import ClientManagementApp
from reports_interface import ReportsManagementApp

class MainMenu:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("Sistema de Gerenciamento")
        
        # Configurar tamanho e centralizar
        self.root.state("zoomed")  # Maximiza a janela
        
        # Criar widgets
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(self.main_frame, text="Sistema de Gerenciamento", font=("Helvetica", 16, "bold")).pack(pady=20)
        
        # Botões do menu
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=50)
        
        # Botão para Caixa
        billing_btn = ttk.Button(
            button_frame, 
            text="Caixa / Cobrança", 
            command=self.open_billing_system,
            width=30,
            style=\'Big.TButton\'
        )
        billing_btn.pack(pady=15)
        
        # Botão para Gerenciamento de Estoque
        product_btn = ttk.Button(
            button_frame, 
            text="Gerenciamento de Estoque", 
            command=self.open_product_management,
            width=30,
            style=\'Big.TButton\'
        )
        product_btn.pack(pady=15)
        
        # Botão para Gerenciamento de Notas
        sales_btn = ttk.Button(
            button_frame, 
            text="Gerenciamento de Notas", 
            command=self.open_sales_management,
            width=30,
            style=\'Big.TButton\'
        )
        sales_btn.pack(pady=15)
        
        # Botão para Gerenciamento de Clientes
        client_btn = ttk.Button(
            button_frame, 
            text="Gerenciamento de Clientes", 
            command=self.open_client_management,
            width=30,
            style=\'Big.TButton\'
        )
        client_btn.pack(pady=15)
        
        # Botão para Gerenciamento de Usuários
        user_btn = ttk.Button(
            button_frame, 
            text="Gerenciamento de Usuários", 
            command=self.open_user_management,
            width=30,
            style=\'Big.TButton\'
        )
        user_btn.pack(pady=15)
        
        # Botão para Relatórios de Vendas (Admin)
        reports_btn = ttk.Button(
            button_frame, 
            text="Relatórios de Vendas (Admin)", 
            command=self.open_reports_management,
            width=30,
            style=\'Big.TButton\'
        )
        reports_btn.pack(pady=15)
        
        # Botão para Sair
        exit_btn = ttk.Button(
            button_frame, 
            text="Sair", 
            command=self.root.quit,
            width=30,
            style=\'Big.TButton\'
        )
        exit_btn.pack(pady=15)
        
        # Configurar estilo para botões grandes
        style = ttk.Style()
        style.configure(\'Big.TButton\', font=(\'Helvetica\', 12), padding=10)
        
        # Barra de status
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(
            self.status_frame, 
            text=f"Logado como: {self.current_user[3]} ({\'Admin\' if bool(self.current_user[5]) else \'Usuário\'})"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
    
    def open_billing_system(self):
        """Abre o sistema de caixa/cobrança"""
        self.root.withdraw()  # Esconde a janela do menu
        billing_window = tk.Toplevel()
        app = BillingSystem(billing_window, self.current_user)
        billing_window.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(billing_window))
    
    def open_product_management(self):
        """Abre a interface de gerenciamento de produtos"""
        self.root.withdraw()  # Esconde a janela do menu
        product_window = tk.Toplevel()
        app = ProductManagementApp(product_window, self.current_user)
        product_window.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(product_window))
    
    def open_sales_management(self):
        """Abre a interface de gerenciamento de notas"""
        self.root.withdraw()  # Esconde a janela do menu
        sales_window = tk.Toplevel()
        app = SalesManagementApp(sales_window, self.current_user)
        sales_window.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(sales_window))
    
    def open_client_management(self):
        """Abre a interface de gerenciamento de clientes"""
        self.root.withdraw()  # Esconde a janela do menu
        client_window = tk.Toplevel()
        app = ClientManagementApp(client_window, self.current_user)
        client_window.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(client_window))
    
    def open_user_management(self):
        """Abre a interface de gerenciamento de usuários"""
        # Verificar se o usuário é admin
        if not bool(self.current_user[5]):
            tk.messagebox.showerror("Acesso Negado", "Apenas administradores podem acessar o gerenciamento de usuários")
            return
        
        self.root.withdraw()  # Esconde a janela do menu
        user_window = tk.Toplevel()
        app = UserManagementApp(user_window, self.current_user)
        user_window.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(user_window))
    
    def open_reports_management(self):
        """Abre a interface de relatórios de vendas (apenas para admins)"""
        if not bool(self.current_user[5]):
            tk.messagebox.showerror("Acesso Negado", "Apenas administradores podem acessar os relatórios de vendas.")
            return
        
        self.root.withdraw()  # Esconde a janela do menu
        reports_window = tk.Toplevel()
        app = ReportsManagementApp(reports_window, self.current_user)
        reports_window.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(reports_window))
    
    def on_child_close(self, child_window):
        """Função chamada quando uma janela filha é fechada"""
        child_window.destroy()
        self.root.deiconify()  # Mostra novamente a janela do menu