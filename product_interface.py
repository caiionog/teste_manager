import tkinter as tk
from tkinter import ttk, messagebox
from database import *

class ProductManagementApp:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("Gerenciamento de Estoque")
        
        # Configurar tamanho e centralizar
        self.root.state('zoomed')  # Maximiza a janela
        
        # Verificar se o usuário atual é admin
        self.is_admin = bool(current_user[5])  # is_admin está na posição 5
        
        # Criar widgets
        self.create_widgets()
        
        # Carregar dados
        self.load_products()
        
    def create_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Barra de ferramentas
        self.toolbar_frame = ttk.Frame(self.main_frame)
        self.toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.add_button = ttk.Button(self.toolbar_frame, text="Adicionar Produto", command=self.show_add_product_dialog)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.edit_button = ttk.Button(self.toolbar_frame, text="Editar Produto", command=self.show_edit_product_dialog)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(self.toolbar_frame, text="Excluir Produto", command=self.delete_product)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.refresh_button = ttk.Button(self.toolbar_frame, text="Atualizar", command=self.load_products)
        self.refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Barra de pesquisa
        self.search_frame = ttk.Frame(self.toolbar_frame)
        self.search_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(self.search_frame, text="Pesquisar:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(self.search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_button = ttk.Button(self.search_frame, text="Buscar", command=self.search_products)
        self.search_button.pack(side=tk.LEFT)
        self.search_entry.bind('<Return>', lambda event: self.search_products())
        
        # Treeview para exibir produtos
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Nome", "Categoria", "Preço", "Quantidade", "Mínimo", "Fornecedor", "Código")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        
        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Preço", text="Preço (R$)")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Mínimo", text="Mínimo")
        self.tree.heading("Fornecedor", text="Fornecedor")
        self.tree.heading("Código", text="Código")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Nome", width=150)
        self.tree.column("Categoria", width=100)
        self.tree.column("Preço", width=80, anchor=tk.E)
        self.tree.column("Quantidade", width=80, anchor=tk.CENTER)
        self.tree.column("Mínimo", width=80, anchor=tk.CENTER)
        self.tree.column("Fornecedor", width=150)
        self.tree.column("Código", width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Barra de status
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_frame, text=f"Logado como: {self.current_user[3]} ({'Admin' if self.is_admin else 'Usuário'})")
        self.status_label.pack(side=tk.LEFT)
        
        # Desabilitar botões se não for admin
        if not self.is_admin:
            self.add_button.config(state=tk.DISABLED)
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
    
    def load_products(self):
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Carregar produtos do banco de dados
        conn = create_connection()
        if conn is not None:
            products = get_all_products(conn)
            conn.close()
            
            for product in products:
                self.tree.insert("", tk.END, values=(
                    product[0],  # ID
                    product[1],  # Nome
                    product[3],  # Categoria
                    f"{product[4]:.2f}",  # Preço
                    product[5],  # Quantidade
                    product[6],  # Mínimo
                    product[7],  # Fornecedor
                    product[8]   # Código de barras
                ))
    
    def search_products(self):
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            self.load_products()
            return
        
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar produtos
        conn = create_connection()
        if conn is not None:
            products = search_products(conn, search_term)
            conn.close()
            
            for product in products:
                self.tree.insert("", tk.END, values=(
                    product[0],  # ID
                    product[1],  # Nome
                    product[3],  # Categoria
                    f"{product[4]:.2f}",  # Preço
                    product[5],  # Quantidade
                    product[6],  # Mínimo
                    product[7],  # Fornecedor
                    product[8]   # Código de barras
                ))
    
    def show_add_product_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Adicionar Novo Produto")
        
        # Centralizar a janela
        window_width = 500
        window_height = 400
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Frame principal
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Widgets
        ttk.Label(frame, text="Nome do Produto:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(frame, text="Descrição:").grid(row=1, column=0, sticky=tk.W, pady=5)
        description_entry = ttk.Entry(frame)
        description_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(frame, text="Categoria:").grid(row=2, column=0, sticky=tk.W, pady=5)
        category_entry = ttk.Entry(frame)
        category_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(frame, text="Preço (R$):").grid(row=3, column=0, sticky=tk.W, pady=5)
        price_entry = ttk.Entry(frame)
        price_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(frame, text="Quantidade:").grid(row=4, column=0, sticky=tk.W, pady=5)
        quantity_entry = ttk.Entry(frame)
        quantity_entry.grid(row=4, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(frame, text="Quantidade Mínima:").grid(row=5, column=0, sticky=tk.W, pady=5)
        min_quantity_entry = ttk.Entry(frame)
        min_quantity_entry.grid(row=5, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(frame, text="Fornecedor:").grid(row=6, column=0, sticky=tk.W, pady=5)
        supplier_entry = ttk.Entry(frame)
        supplier_entry.grid(row=6, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(frame, text="Código de Barras:").grid(row=7, column=0, sticky=tk.W, pady=5)
        barcode_entry = ttk.Entry(frame)
        barcode_entry.grid(row=7, column=1, sticky=tk.EW, pady=5)
        
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Salvar", command=lambda: self.add_product(
            dialog,
            name_entry.get(),
            description_entry.get(),
            category_entry.get(),
            price_entry.get(),
            quantity_entry.get(),
            min_quantity_entry.get(),
            supplier_entry.get(),
            barcode_entry.get()
        )).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Configurar expansão das colunas
        frame.columnconfigure(1, weight=1)
    
    def add_product(self, dialog, name, description, category, price, quantity, min_quantity, supplier, barcode):
        if not name or not price or not quantity:
            messagebox.showerror("Erro", "Por favor, preencha pelo menos nome, preço e quantidade")
            return
        
        try:
            price = float(price)
            quantity = int(quantity)
            min_quantity = int(min_quantity) if min_quantity else 0
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número decimal e quantidade deve ser um número inteiro")
            return
        
        conn = create_connection()
        if conn is not None:
            product_id = add_product(conn, name, description, category, price, quantity, min_quantity, supplier, barcode)
            conn.close()
            
            if product_id:
                messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
                dialog.destroy()
                self.load_products()
            else:
                messagebox.showerror("Erro", "Não foi possível adicionar o produto. O código de barras pode já estar em uso.")
    
    def show_edit_product_dialog(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione um produto para editar")
            return
        
        product_id = self.tree.item(selected_item[0], "values")[0]
        
        conn = create_connection()
        if conn is not None:
            product = get_product_by_id(conn, product_id)
            conn.close()
            
            if product:
                dialog = tk.Toplevel(self.root)
                dialog.title("Editar Produto")
                
                # Centralizar a janela
                window_width = 500
                window_height = 400
                screen_width = dialog.winfo_screenwidth()
                screen_height = dialog.winfo_screenheight()
                x = (screen_width - window_width) // 2
                y = (screen_height - window_height) // 2
                dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
                
                # Frame principal
                frame = ttk.Frame(dialog, padding="10")
                frame.pack(fill=tk.BOTH, expand=True)
                
                # Widgets
                ttk.Label(frame, text="Nome do Produto:").grid(row=0, column=0, sticky=tk.W, pady=5)
                name_entry = ttk.Entry(frame)
                name_entry.insert(0, product[1])
                name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
                
                ttk.Label(frame, text="Descrição:").grid(row=1, column=0, sticky=tk.W, pady=5)
                description_entry = ttk.Entry(frame)
                description_entry.insert(0, product[2])
                description_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
                
                ttk.Label(frame, text="Categoria:").grid(row=2, column=0, sticky=tk.W, pady=5)
                category_entry = ttk.Entry(frame)
                category_entry.insert(0, product[3])
                category_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)
                
                ttk.Label(frame, text="Preço (R$):").grid(row=3, column=0, sticky=tk.W, pady=5)
                price_entry = ttk.Entry(frame)
                price_entry.insert(0, str(product[4]))
                price_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)
                
                ttk.Label(frame, text="Quantidade:").grid(row=4, column=0, sticky=tk.W, pady=5)
                quantity_entry = ttk.Entry(frame)
                quantity_entry.insert(0, str(product[5]))
                quantity_entry.grid(row=4, column=1, sticky=tk.EW, pady=5)
                
                ttk.Label(frame, text="Quantidade Mínima:").grid(row=5, column=0, sticky=tk.W, pady=5)
                min_quantity_entry = ttk.Entry(frame)
                min_quantity_entry.insert(0, str(product[6]))
                min_quantity_entry.grid(row=5, column=1, sticky=tk.EW, pady=5)
                
                ttk.Label(frame, text="Fornecedor:").grid(row=6, column=0, sticky=tk.W, pady=5)
                supplier_entry = ttk.Entry(frame)
                supplier_entry.insert(0, product[7] if product[7] else "")
                supplier_entry.grid(row=6, column=1, sticky=tk.EW, pady=5)
                
                ttk.Label(frame, text="Código de Barras:").grid(row=7, column=0, sticky=tk.W, pady=5)
                barcode_entry = ttk.Entry(frame)
                barcode_entry.insert(0, product[8] if product[8] else "")
                barcode_entry.grid(row=7, column=1, sticky=tk.EW, pady=5)
                
                button_frame = ttk.Frame(frame)
                button_frame.grid(row=8, column=0, columnspan=2, pady=10)
                
                ttk.Button(button_frame, text="Salvar", command=lambda: self.update_product(
                    dialog,
                    product[0],
                    name_entry.get(),
                    description_entry.get(),
                    category_entry.get(),
                    price_entry.get(),
                    quantity_entry.get(),
                    min_quantity_entry.get(),
                    supplier_entry.get(),
                    barcode_entry.get()
                )).pack(side=tk.LEFT, padx=5)
                
                ttk.Button(button_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
                
                # Configurar expansão das colunas
                frame.columnconfigure(1, weight=1)
    
    def update_product(self, dialog, product_id, name, description, category, price, quantity, min_quantity, supplier, barcode):
        if not name or not price or not quantity:
            messagebox.showerror("Erro", "Por favor, preencha pelo menos nome, preço e quantidade")
            return
        
        try:
            price = float(price)
            quantity = int(quantity)
            min_quantity = int(min_quantity) if min_quantity else 0
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número decimal e quantidade deve ser um número inteiro")
            return
        
        conn = create_connection()
        if conn is not None:
            success = update_product(conn, product_id, name, description, category, price, quantity, min_quantity, supplier, barcode)
            conn.close()
            
            if success:
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                dialog.destroy()
                self.load_products()
            else:
                messagebox.showerror("Erro", "Não foi possível atualizar o produto. O código de barras pode já estar em uso.")
    
    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione um produto para excluir")
            return
        
        product_id = self.tree.item(selected_item[0], "values")[0]
        product_name = self.tree.item(selected_item[0], "values")[1]
        
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o produto '{product_name}'?"):
            conn = create_connection()
            if conn is not None:
                success = delete_product(conn, product_id)
                conn.close()
                
                if success:
                    messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
                    self.load_products()
                else:
                    messagebox.showerror("Erro", "Não foi possível excluir o produto")