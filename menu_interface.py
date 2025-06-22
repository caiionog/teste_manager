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
        
        # Configurar cores e estilo
        self.setup_styles()
        
        # Criar widgets
        self.create_widgets()
    
    def setup_styles(self):
        """Configurar estilos personalizados para os botões"""
        style = ttk.Style()
        
        # Estilo para botão do Caixa (Verde)
        style.configure('Caixa.TButton', 
                       font=('Helvetica', 14, 'bold'),
                       padding=(20, 15),
                       background='#4CAF50',
                       foreground='white')
        
        # Estilo para botão de Estoque (Azul)
        style.configure('Estoque.TButton', 
                       font=('Helvetica', 14, 'bold'),
                       padding=(20, 15),
                       background='#2196F3',
                       foreground='white')
        
        # Estilo para botão de Notas (Laranja)
        style.configure('Notas.TButton', 
                       font=('Helvetica', 14, 'bold'),
                       padding=(20, 15),
                       background='#FF9800',
                       foreground='white')
        
        # Estilo para botão de Clientes (Roxo)
        style.configure('Clientes.TButton', 
                       font=('Helvetica', 14, 'bold'),
                       padding=(20, 15),
                       background='#9C27B0',
                       foreground='white')
        
        # Estilo para botão de Usuários (Vermelho)
        style.configure('Usuarios.TButton', 
                       font=('Helvetica', 14, 'bold'),
                       padding=(20, 15),
                       background='#F44336',
                       foreground='white')
        
        # Estilo para botão de Relatórios (Cinza escuro)
        style.configure('Relatorios.TButton', 
                       font=('Helvetica', 14, 'bold'),
                       padding=(20, 15),
                       background='#607D8B',
                       foreground='white')
        
        # Estilo para botão de Sair (Cinza)
        style.configure('Sair.TButton', 
                       font=('Helvetica', 12, 'bold'),
                       padding=(15, 10),
                       background='#9E9E9E',
                       foreground='white')
    
    def create_widgets(self):
        # Frame principal com cor de fundo
        self.main_frame = ttk.Frame(self.root, padding="30")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título principal
        title_label = ttk.Label(
            self.main_frame, 
            text="Sistema de Gerenciamento", 
            font=("Helvetica", 24, "bold"),
            foreground="#2C3E50"
        )
        title_label.pack(pady=(0, 30))
        
        # Subtítulo
        subtitle_label = ttk.Label(
            self.main_frame, 
            text="Selecione o módulo desejado", 
            font=("Helvetica", 14),
            foreground="#7F8C8D"
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Frame para os botões em grid
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(expand=True)
        
        # Configurar grid com 2 colunas e 3 linhas
        buttons_frame.grid_columnconfigure(0, weight=1, pad=20)
        buttons_frame.grid_columnconfigure(1, weight=1, pad=20)
        
        # Botão para Caixa (0,0) - Verde
        caixa_frame = ttk.Frame(buttons_frame, relief="raised", borderwidth=2)
        caixa_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew", ipadx=10, ipady=10)
        
        ttk.Label(caixa_frame, text="💰", font=("Arial", 24)).pack(pady=(10, 5))
        caixa_btn = ttk.Button(
            caixa_frame, 
            text="Caixa / Cobrança", 
            command=self.open_billing_system,
            style='Caixa.TButton',
            width=25
        )
        caixa_btn.pack(pady=(0, 10))
        ttk.Label(caixa_frame, text="Vendas e faturamento", font=("Arial", 10), foreground="#666").pack()
        
        # Botão para Estoque (0,1) - Azul
        estoque_frame = ttk.Frame(buttons_frame, relief="raised", borderwidth=2)
        estoque_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew", ipadx=10, ipady=10)
        
        ttk.Label(estoque_frame, text="📦", font=("Arial", 24)).pack(pady=(10, 5))
        estoque_btn = ttk.Button(
            estoque_frame, 
            text="Gerenciar Estoque", 
            command=self.open_product_management,
            style='Estoque.TButton',
            width=25
        )
        estoque_btn.pack(pady=(0, 10))
        ttk.Label(estoque_frame, text="Produtos e inventário", font=("Arial", 10), foreground="#666").pack()
        
        # Botão para Notas (1,0) - Laranja
        notas_frame = ttk.Frame(buttons_frame, relief="raised", borderwidth=2)
        notas_frame.grid(row=1, column=0, padx=15, pady=15, sticky="nsew", ipadx=10, ipady=10)
        
        ttk.Label(notas_frame, text="📄", font=("Arial", 24)).pack(pady=(10, 5))
        notas_btn = ttk.Button(
            notas_frame, 
            text="Gerenciar Notas", 
            command=self.open_sales_management,
            style='Notas.TButton',
            width=25
        )
        notas_btn.pack(pady=(0, 10))
        ttk.Label(notas_frame, text="Notas fiscais e vendas", font=("Arial", 10), foreground="#666").pack()
        
        # Botão para Clientes (1,1) - Roxo
        clientes_frame = ttk.Frame(buttons_frame, relief="raised", borderwidth=2)
        clientes_frame.grid(row=1, column=1, padx=15, pady=15, sticky="nsew", ipadx=10, ipady=10)
        
        ttk.Label(clientes_frame, text="👥", font=("Arial", 24)).pack(pady=(10, 5))
        clientes_btn = ttk.Button(
            clientes_frame, 
            text="Gerenciar Clientes", 
            command=self.open_client_management,
            style='Clientes.TButton',
            width=25
        )
        clientes_btn.pack(pady=(0, 10))
        ttk.Label(clientes_frame, text="Cadastro de clientes", font=("Arial", 10), foreground="#666").pack()
        
        # Botão para Usuários (2,0) - Vermelho
        usuarios_frame = ttk.Frame(buttons_frame, relief="raised", borderwidth=2)
        usuarios_frame.grid(row=2, column=0, padx=15, pady=15, sticky="nsew", ipadx=10, ipady=10)
        
        ttk.Label(usuarios_frame, text="👤", font=("Arial", 24)).pack(pady=(10, 5))
        usuarios_btn = ttk.Button(
            usuarios_frame, 
            text="Gerenciar Usuários", 
            command=self.open_user_management,
            style='Usuarios.TButton',
            width=25
        )
        usuarios_btn.pack(pady=(0, 10))
        ttk.Label(usuarios_frame, text="Usuários do sistema", font=("Arial", 10), foreground="#666").pack()
        
        # Botão para Relatórios (2,1) - Cinza escuro
        relatorios_frame = ttk.Frame(buttons_frame, relief="raised", borderwidth=2)
        relatorios_frame.grid(row=2, column=1, padx=15, pady=15, sticky="nsew", ipadx=10, ipady=10)
        
        ttk.Label(relatorios_frame, text="📊", font=("Arial", 24)).pack(pady=(10, 5))
        relatorios_btn = ttk.Button(
            relatorios_frame, 
            text="Relatórios (Admin)", 
            command=self.open_reports_management,
            style='Relatorios.TButton',
            width=25
        )
        relatorios_btn.pack(pady=(0, 10))
        ttk.Label(relatorios_frame, text="Relatórios de vendas", font=("Arial", 10), foreground="#666").pack()
        
        # Configurar expansão uniforme das células do grid
        for i in range(3):
            buttons_frame.grid_rowconfigure(i, weight=1)
        
        # Botão de Sair centralizado na parte inferior
        sair_frame = ttk.Frame(self.main_frame)
        sair_frame.pack(pady=(40, 20))
        
        sair_btn = ttk.Button(
            sair_frame, 
            text="Sair do Sistema", 
            command=self.root.quit,
            style='Sair.TButton',
            width=20
        )
        sair_btn.pack()
        
        # Barra de status na parte inferior
        self.status_frame = ttk.Frame(self.root, relief="sunken", borderwidth=1)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(
            self.status_frame, 
            text=f"Logado como: {self.current_user[3]} ({'Admin' if bool(self.current_user[5]) else 'Usuário'})",
            font=("Arial", 10),
            padding=(10, 5)
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Data/hora na barra de status
        import datetime
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        time_label = ttk.Label(
            self.status_frame,
            text=now,
            font=("Arial", 10),
            padding=(10, 5)
        )
        time_label.pack(side=tk.RIGHT)
    
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