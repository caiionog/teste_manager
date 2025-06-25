import tkinter as tk
from tkinter import ttk, messagebox
from database import *
import datetime

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Sistema de Gerenciamento - Login")
        self.on_login_success = on_login_success
        
        # Configurar janela
        window_width = 450
        window_height = 550
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
        
        # Configurar cor de fundo
        self.root.configure(bg='#f0f0f0')
        
        # Configurar estilos
        self.setup_styles()
        
        # Criar widgets
        self.create_widgets()
        
        # Focar no campo de usuário
        self.username_entry.focus()
        
    def setup_styles(self):
        """Configurar estilos personalizados"""
        style = ttk.Style()
        
        # Estilo para o botão de login
        style.configure('Login.TButton',
                       font=('Helvetica', 12, 'bold'),
                       padding=(20, 10))
        
        # Estilo para labels principais
        style.configure('Title.TLabel',
                       font=('Helvetica', 24, 'bold'),
                       foreground='#2c3e50',
                       background='#f0f0f0')
        
        style.configure('Subtitle.TLabel',
                       font=('Helvetica', 12),
                       foreground='#7f8c8d',
                       background='#f0f0f0')
        
        # Estilo para campos de entrada
        style.configure('Login.TEntry',
                       font=('Helvetica', 11),
                       padding=(10, 8))
        
    def create_widgets(self):
        # Frame principal com gradiente visual
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Cabeçalho com logo/ícone
        header_frame = tk.Frame(main_frame, bg='#f0f0f0')
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Ícone do sistema (usando emoji como placeholder)
        icon_label = tk.Label(header_frame, text="🏢", font=("Arial", 48), bg='#f0f0f0')
        icon_label.pack()
        
        # Título principal
        title_label = ttk.Label(header_frame, text="Sistema de Gerenciamento", style='Title.TLabel')
        title_label.pack(pady=(10, 5))
        
        # Subtítulo
        subtitle_label = ttk.Label(header_frame, text="Faça login para continuar", style='Subtitle.TLabel')
        subtitle_label.pack()
        
        # Frame do formulário de login
        login_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=1)
        login_frame.pack(fill=tk.X, pady=20, padx=20)
        
        # Padding interno do formulário
        form_frame = tk.Frame(login_frame, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Campo de usuário
        user_frame = tk.Frame(form_frame, bg='white')
        user_frame.pack(fill=tk.X, pady=(0, 20))
        
        user_label = tk.Label(user_frame, text="👤 Usuário", font=('Helvetica', 11, 'bold'), 
                             bg='white', fg='#2c3e50')
        user_label.pack(anchor='w', pady=(0, 5))
        
        self.username_entry = ttk.Entry(user_frame, style='Login.TEntry', width=25)
        self.username_entry.pack(fill=tk.X)
        
        # Campo de senha
        pass_frame = tk.Frame(form_frame, bg='white')
        pass_frame.pack(fill=tk.X, pady=(0, 25))
        
        pass_label = tk.Label(pass_frame, text="🔒 Senha", font=('Helvetica', 11, 'bold'), 
                             bg='white', fg='#2c3e50')
        pass_label.pack(anchor='w', pady=(0, 5))
        
        self.password_entry = ttk.Entry(pass_frame, show="*", style='Login.TEntry', width=25)
        self.password_entry.pack(fill=tk.X)
        
        # Botão de login
        self.login_button = ttk.Button(form_frame, text="🚀 Entrar", command=self.login, style='Login.TButton')
        self.login_button.pack(fill=tk.X, pady=(10, 0))
        
        # Informações de acesso padrão
        info_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='solid', bd=1)
        info_frame.pack(fill=tk.X, pady=(20, 0), padx=20)
        
        info_content = tk.Frame(info_frame, bg='#ecf0f1')
        info_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        info_title = tk.Label(info_content, text="ℹ️ Acesso Padrão", font=('Helvetica', 10, 'bold'), 
                             bg='#ecf0f1', fg='#2c3e50')
        info_title.pack(anchor='w')
        
        info_text = tk.Label(info_content, text="Usuário: admin\nSenha: admin123", 
                            font=('Helvetica', 9), bg='#ecf0f1', fg='#7f8c8d', justify='left')
        info_text.pack(anchor='w', pady=(5, 0))
        
        # Rodapé com data/hora
        footer_frame = tk.Frame(main_frame, bg='#f0f0f0')
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        footer_label = tk.Label(footer_frame, text=f"📅 {current_time}", 
                               font=('Helvetica', 9), bg='#f0f0f0', fg='#95a5a6')
        footer_label.pack()
        
        # Bind Enter key to login
        self.root.bind("<Return>", lambda event: self.login())
        
        # Bind Tab para navegação entre campos
        self.username_entry.bind("<Tab>", lambda event: self.password_entry.focus())
        
        # Efeitos visuais nos campos
        self.username_entry.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event))
        self.username_entry.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event))
        self.password_entry.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event))
        self.password_entry.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event))
        
        # Efeito hover no botão
        self.login_button.bind("<Enter>", self.on_button_hover)
        self.login_button.bind("<Leave>", self.on_button_leave)
        
    def on_entry_focus_in(self, event):
        """Efeito visual quando campo recebe foco"""
        event.widget.configure(style='Focused.TEntry')
        
    def on_entry_focus_out(self, event):
        """Efeito visual quando campo perde foco"""
        event.widget.configure(style='Login.TEntry')
        
    def on_button_hover(self, event):
        """Efeito hover no botão"""
        style = ttk.Style()
        style.configure('Hover.TButton',
                       font=('Helvetica', 12, 'bold'),
                       padding=(20, 10))
        self.login_button.configure(style='Hover.TButton')
        
    def on_button_leave(self, event):
        """Remove efeito hover do botão"""
        self.login_button.configure(style='Login.TButton')
        
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validação visual dos campos
        if not username:
            self.show_field_error(self.username_entry, "Campo obrigatório")
            return
            
        if not password:
            self.show_field_error(self.password_entry, "Campo obrigatório")
            return
        
        # Desabilitar botão durante login
        self.login_button.configure(text="🔄 Verificando...", state='disabled')
        self.root.update()
        
        # Simular delay de autenticação
        self.root.after(500, lambda: self.perform_login(username, password))
    
    def perform_login(self, username, password):
        """Realiza o login após delay visual"""
        conn = create_connection()
        if conn is not None:
            user = login_user(conn, username, password)
            conn.close()
            
            if user:
                # Sucesso - efeito visual
                self.login_button.configure(text="✅ Sucesso!", style='Success.TButton')
                self.root.after(500, lambda: self.complete_login(user))
            else:
                # Erro - efeito visual
                self.login_button.configure(text="❌ Erro", style='Error.TButton')
                self.root.after(1000, self.reset_login_button)
                self.show_login_error()
        else:
            self.login_button.configure(text="❌ Erro de Conexão", style='Error.TButton')
            self.root.after(1000, self.reset_login_button)
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados")
    
    def complete_login(self, user):
        """Completa o processo de login"""
        self.root.destroy()
        self.on_login_success(user)
    
    def reset_login_button(self):
        """Reseta o botão de login"""
        self.login_button.configure(text="🚀 Entrar", state='normal', style='Login.TButton')
    
    def show_field_error(self, field, message):
        """Mostra erro visual no campo"""
        # Criar tooltip de erro temporário
        error_window = tk.Toplevel(self.root)
        error_window.wm_overrideredirect(True)
        error_window.configure(bg='#e74c3c')
        
        # Posicionar próximo ao campo
        x = field.winfo_rootx()
        y = field.winfo_rooty() + field.winfo_height() + 5
        error_window.geometry(f"+{x}+{y}")
        
        error_label = tk.Label(error_window, text=message, bg='#e74c3c', fg='white', 
                              font=('Helvetica', 9), padx=10, pady=5)
        error_label.pack()
        
        # Remover tooltip após 2 segundos
        self.root.after(2000, error_window.destroy)
        
        # Focar no campo com erro
        field.focus()
    
    def show_login_error(self):
        """Mostra erro de login com efeito visual"""
        error_window = tk.Toplevel(self.root)
        error_window.title("Erro de Login")
        error_window.geometry("300x150")
        error_window.resizable(False, False)
        error_window.configure(bg='white')
        
        # Centralizar janela de erro
        error_window.transient(self.root)
        error_window.grab_set()
        
        # Posicionar no centro da janela principal
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
        error_window.geometry(f"300x150+{x}+{y}")
        
        # Conteúdo da janela de erro
        error_frame = tk.Frame(error_window, bg='white')
        error_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Ícone de erro
        icon_label = tk.Label(error_frame, text="❌", font=("Arial", 24), bg='white')
        icon_label.pack(pady=(0, 10))
        
        # Mensagem de erro
        message_label = tk.Label(error_frame, text="Usuário ou senha incorretos", 
                                font=('Helvetica', 11), bg='white', fg='#e74c3c')
        message_label.pack(pady=(0, 15))
        
        # Botão OK
        ok_button = ttk.Button(error_frame, text="OK", command=error_window.destroy)
        ok_button.pack()
        
        # Focar no botão OK
        ok_button.focus()
        
        # Bind Enter para fechar
        error_window.bind("<Return>", lambda event: error_window.destroy())

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
        
        self.status_label = ttk.Label(self.status_frame, text=f"Logado como: {self.current_user[3]} ({'Admin' if self.is_admin else 'Usuário'}) ")
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
        dialog = tk.Toplevel(self.root)
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
                dialog = tk.Toplevel(self.root)
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
        
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o usuário '{username}'?"):
            conn = create_connection()
            if conn is not None:
                success = delete_user(conn, user_id)
                conn.close()
                
                if success:
                    messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                    self.load_users()
                else:
                    messagebox.showerror("Erro", "Não foi possível excluir o usuário")

