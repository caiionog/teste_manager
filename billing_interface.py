import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import filedialog
from database import *
from datetime import datetime
import os
from fpdf import FPDF

class BillingSystem:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("Sistema de Cobrança")
        
        # Variáveis da venda
        self.cart = []
        self.customer_name = ""
        self.customer_doc = ""
        self.payment_method = "Dinheiro"
        
        # Configurar tamanho e centralizar
        self.root.state("zoomed")  # Maximiza a janela
        
        # Criar widgets
        self.create_widgets()
        
        # Carregar produtos disponíveis
        self.load_products()
    
    def create_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame superior (produtos e carrinho)
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de produtos disponíveis
        products_frame = ttk.LabelFrame(top_frame, text="Produtos Disponíveis", padding="10")
        products_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview para produtos
        self.products_tree = ttk.Treeview(products_frame, columns=("ID", "Nome", "Preço", "Estoque"), show="headings")
        self.products_tree.heading("ID", text="ID")
        self.products_tree.heading("Nome", text="Nome")
        self.products_tree.heading("Preço", text="Preço (R$)")
        self.products_tree.heading("Estoque", text="Estoque")
        
        self.products_tree.column("ID", width=50, anchor=tk.CENTER)
        self.products_tree.column("Nome", width=150)
        self.products_tree.column("Preço", width=80, anchor=tk.E)
        self.products_tree.column("Estoque", width=80, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(products_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.products_tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame do carrinho
        cart_frame = ttk.LabelFrame(top_frame, text="Carrinho de Compras", padding="10")
        cart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview para carrinho
        self.cart_tree = ttk.Treeview(cart_frame, columns=("ID", "Nome", "Qtd", "Preço", "Total"), show="headings")
        self.cart_tree.heading("ID", text="ID")
        self.cart_tree.heading("Nome", text="Nome")
        self.cart_tree.heading("Qtd", text="Qtd")
        self.cart_tree.heading("Preço", text="Preço (R$)")
        self.cart_tree.heading("Total", text="Total (R$)")
        
        self.cart_tree.column("ID", width=50, anchor=tk.CENTER)
        self.cart_tree.column("Nome", width=150)
        self.cart_tree.column("Qtd", width=60, anchor=tk.CENTER)
        self.cart_tree.column("Preço", width=80, anchor=tk.E)
        self.cart_tree.column("Total", width=80, anchor=tk.E)
        
        # Scrollbar
        cart_scrollbar = ttk.Scrollbar(cart_frame, orient=tk.VERTICAL, command=self.cart_tree.yview)
        self.cart_tree.configure(yscroll=cart_scrollbar.set)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame de botões
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        self.add_button = ttk.Button(buttons_frame, text="Adicionar →", command=self.add_to_cart)
        self.add_button.pack(pady=5, fill=tk.X)
        
        self.remove_button = ttk.Button(buttons_frame, text="← Remover", command=self.remove_from_cart)
        self.remove_button.pack(pady=5, fill=tk.X)
        
        self.clear_button = ttk.Button(buttons_frame, text="Limpar Carrinho", command=self.clear_cart)
        self.clear_button.pack(pady=5, fill=tk.X)
        
        # Frame inferior (informações da venda)
        bottom_frame = ttk.LabelFrame(self.main_frame, text="Informações da Venda", padding="10")
        bottom_frame.pack(fill=tk.X, pady=5)
        
        # Cliente
        ttk.Label(bottom_frame, text="Cliente:").grid(row=0, column=0, sticky=tk.W)
        self.customer_entry = ttk.Entry(bottom_frame, width=30)
        self.customer_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(bottom_frame, text="CPF/CNPJ:").grid(row=0, column=2, sticky=tk.W)
        self.doc_entry = ttk.Entry(bottom_frame, width=20)
        self.doc_entry.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        ttk.Label(bottom_frame, text="Pagamento:").grid(row=1, column=0, sticky=tk.W)
        self.payment_var = tk.StringVar(value="Dinheiro")
        payment_options = ["Dinheiro", "Cartão Débito", "Cartão Crédito", "PIX", "Transferência"]
        self.payment_combobox = ttk.Combobox(bottom_frame, textvariable=self.payment_var, values=payment_options, width=15)
        self.payment_combobox.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(bottom_frame, text="Subtotal:").grid(row=2, column=0, sticky=tk.W)
        self.subtotal_label = ttk.Label(bottom_frame, text="R$ 0.00", font=("Helvetica", 10, "bold"))
        self.subtotal_label.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(bottom_frame, text="Desconto:").grid(row=2, column=2, sticky=tk.W)
        self.discount_entry = ttk.Entry(bottom_frame, width=10)
        self.discount_entry.insert(0, "0.00")
        self.discount_entry.grid(row=2, column=3, sticky=tk.W, padx=5)
        
        ttk.Label(bottom_frame, text="Total:").grid(row=3, column=0, sticky=tk.W)
        self.total_label = ttk.Label(bottom_frame, text="R$ 0.00", font=("Helvetica", 12, "bold"))
        self.total_label.grid(row=3, column=1, sticky=tk.W, padx=5)
        
        action_frame = ttk.Frame(bottom_frame)
        action_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        self.finalize_button = ttk.Button(action_frame, text="Finalizar Venda", command=self.finalize_sale)
        self.finalize_button.pack(side=tk.LEFT, padx=5)
        
        self.print_button = ttk.Button(action_frame, text="Imprimir Nota", command=self.print_receipt)
        self.print_button.pack(side=tk.LEFT, padx=5)
        
        self.pdf_button = ttk.Button(action_frame, text="Salvar como PDF", command=self.save_as_pdf)
        self.pdf_button.pack(side=tk.LEFT, padx=5)
        
        self.discount_entry.bind("<KeyRelease>", self.update_totals)
        
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(
            self.status_frame, 
            text=f"Atendente: {self.current_user[3]} | Carrinho: 0 itens"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
    
    def load_products(self):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        conn = create_connection()
        if conn is not None:
            products = get_all_products(conn)
            conn.close()
            
            for product in products:
                if product[5] > 0:  # Só mostra produtos com estoque > 0
                    self.products_tree.insert("", tk.END, values=(
                        product[0],  # ID
                        product[1],  # Nome
                        f"{product[4]:.2f}",  # Preço
                        product[5]   # Quantidade
                    ))
    
    def add_to_cart(self):
        selected_item = self.products_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione um produto para adicionar")
            return
        
        product_id = self.products_tree.item(selected_item[0], "values")[0]
        product_name = self.products_tree.item(selected_item[0], "values")[1]
        price = float(self.products_tree.item(selected_item[0], "values")[2])
        stock = int(self.products_tree.item(selected_item[0], "values")[3])
        
        quantity = simpledialog.askinteger("Quantidade", f"Quantidade de '{product_name}'", minvalue=1, maxvalue=stock)
        if quantity is None or quantity <= 0:
            return
        
        for item in self.cart:
            if item["id"] == product_id:
                item["quantity"] += quantity
                item["total"] = item["quantity"] * price
                self.update_cart_display()
                self.update_totals()
                return
        
        self.cart.append({
            "id": product_id,
            "name": product_name,
            "quantity": quantity,
            "price": price,
            "total": quantity * price
        })
        
        self.update_cart_display()
        self.update_totals()
    
    def remove_from_cart(self):
        selected_item = self.cart_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione um item para remover")
            return
        
        product_id = self.cart_tree.item(selected_item[0], "values")[0]
        
        self.cart = [item for item in self.cart if item["id"] != product_id]
        
        self.update_cart_display()
        self.update_totals()
    
    def clear_cart(self):
        if not self.cart:
            return
            
        if messagebox.askyesno("Confirmar", "Deseja limpar todo o carrinho?"):
            self.cart = []
            self.update_cart_display()
            self.update_totals()
    
    def update_cart_display(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        for item in self.cart:
            self.cart_tree.insert("", tk.END, values=(
                item["id"],
                item["name"],
                item["quantity"],
                f"{item['price']:.2f}",
                f"{item['total']:.2f}"
            ))
        
        self.status_label.config(text=f"Atendente: {self.current_user[3]} | Carrinho: {len(self.cart)} itens")
    
    def update_totals(self, event=None):
        subtotal = sum(item["total"] for item in self.cart)
        
        try:
            discount = float(self.discount_entry.get())
        except ValueError:
            discount = 0.0
            self.discount_entry.delete(0, tk.END)
            self.discount_entry.insert(0, "0.00")
        
        total = max(0, subtotal - discount)
        
        self.subtotal_label.config(text=f"R$ {subtotal:.2f}")
        self.total_label.config(text=f"R$ {total:.2f}")
    
    def finalize_sale(self):
        if not self.cart:
            messagebox.showwarning("Aviso", "O carrinho está vazio")
            return
        
        self.customer_name = self.customer_entry.get().strip()
        self.customer_doc = self.doc_entry.get().strip()
        self.payment_method = self.payment_var.get()
        
        subtotal = sum(item["total"] for item in self.cart)
        try:
            discount = float(self.discount_entry.get())
        except ValueError:
            discount = 0.0
        total = max(0, subtotal - discount)
        
        if not messagebox.askyesno("Confirmar Venda", f"Total da venda: R$ {total:.2f}\n\nConfirmar venda?"):
            return
        
        conn = create_connection()
        if conn is not None:
            try:
                conn.execute("BEGIN TRANSACTION")
                
                sale_id = add_sale(
                    conn,
                    self.customer_name if self.customer_name else "Consumidor Final",
                    self.customer_doc,
                    subtotal,
                    discount,
                    total,
                    self.payment_method,
                    self.current_user[0]
                )
                
                if sale_id:
                    for item in self.cart:
                        add_sale_item(
                            conn,
                            sale_id,
                            item["id"],
                            item["quantity"],
                            item["price"],
                            item["total"]
                        )
                        
                        update_product_quantity(conn, item["id"], item["quantity"])
                    
                    conn.commit()
                    
                    messagebox.showinfo("Sucesso", f"Venda finalizada com sucesso!\nNúmero da nota: {sale_id}")
                    
                    self.cart = []
                    self.customer_entry.delete(0, tk.END)
                    self.doc_entry.delete(0, tk.END)
                    self.discount_entry.delete(0, tk.END)
                    self.discount_entry.insert(0, "0.00")
                    self.update_cart_display()
                    self.update_totals()
                    self.load_products()
                    
                    self.generate_receipt(sale_id)
                    self.save_as_pdf(sale_id)
                else:
                    conn.rollback()
                    messagebox.showerror("Erro", "Não foi possível registrar a venda")
                
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Erro", f"Ocorreu um erro ao registrar a venda:\n{str(e)}")
            
            finally:
                conn.close()
    
    def generate_receipt(self, sale_id):
        conn = create_connection()
        if conn is not None:
            sale, items = get_sale_by_id(conn, sale_id)
            conn.close()
            
            if sale and items:
                receipt_data = {
                    "sale_id": sale[0],
                    "date": sale[1],
                    "customer_name": sale[2],
                    "customer_doc": sale[3],
                    "subtotal": sale[4],
                    "discount": sale[5],
                    "total": sale[6],
                    "payment_method": sale[7],
                    "cashier": self.current_user[3],
                    "seller_id": sale[8],
                    "items": []
                }
                
                for item in items:
                    receipt_data["items"].append({
                        "name": item[6],
                        "quantity": item[3],
                        "unit_price": item[4],
                        "total_price": item[5]
                    })
                
                return receipt_data
            else:
                messagebox.showerror("Erro", "Não foi possível gerar a nota fiscal. Dados da venda não encontrados.")
                return None

    def create_pdf(self, receipt_data):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        
        pdf.cell(0, 10, "NOTA FISCAL", 0, 1, "C")
        pdf.ln(10)
        
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 10, f"Número da Venda: {receipt_data['sale_id']}", 0, 1)
        pdf.cell(0, 10, f"Data: {receipt_data['date']}", 0, 1)
        pdf.cell(0, 10, f"Cliente: {receipt_data['customer_name']}", 0, 1)
        pdf.cell(0, 10, f"CPF/CNPJ: {receipt_data['customer_doc']}", 0, 1)
        pdf.cell(0, 10, f"Atendente: {receipt_data['cashier']} (ID: {receipt_data['seller_id']})")
        pdf.ln(10)
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "ITENS DA VENDA", 0, 1, "C")
        pdf.ln(5)
        
        pdf.set_font("Arial", "B", 10)
        pdf.cell(80, 10, "Produto", 1, 0, "C")
        pdf.cell(30, 10, "Qtd", 1, 0, "C")
        pdf.cell(40, 10, "Preço Unit.", 1, 0, "C")
        pdf.cell(40, 10, "Total", 1, 1, "C")
        
        pdf.set_font("Arial", "", 10)
        for item in receipt_data["items"]:
            pdf.cell(80, 10, item["name"], 1, 0, "L")
            pdf.cell(30, 10, str(item["quantity"]), 1, 0, "C")
            pdf.cell(40, 10, f"R$ {item['unit_price']:.2f}", 1, 0, "R")
            pdf.cell(40, 10, f"R$ {item['total_price']:.2f}", 1, 1, "R")
        
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Subtotal: R$ {receipt_data['subtotal']:.2f}", 0, 1, "R")
        pdf.cell(0, 10, f"Desconto: R$ {receipt_data['discount']:.2f}", 0, 1, "R")
        pdf.cell(0, 10, f"TOTAL: R$ {receipt_data['total']:.2f}", 0, 1, "R")
        pdf.ln(5)
        pdf.cell(0, 10, f"Forma de Pagamento: {receipt_data['payment_method']}", 0, 1)
        
        return pdf

    def print_receipt(self):
        messagebox.showinfo("Imprimir", "Função de impressão não implementada")

    def save_as_pdf(self, sale_id=None):
        if sale_id is None:
            messagebox.showwarning("Aviso", "Nenhuma venda selecionada para salvar")
            return
        
        receipt_data = self.generate_receipt(sale_id)
        if receipt_data:
            pdf = self.create_pdf(receipt_data)
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"NotaFiscal_{receipt_data['sale_id']}.pdf"
            )
            
            if filename:
                pdf.output(filename)
                messagebox.showinfo("Sucesso", f"Nota fiscal salva como: {filename}")

