import tkinter as tk
from tkinter import ttk, messagebox
from database import create_connection, get_sales_by_user, get_all_products, get_user_by_id
from ttkthemes import ThemedTk

class ReportsManagementApp:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("Relatórios de Vendas")
        if isinstance(self.root, ThemedTk):
            self.root.set_theme("black")
        self.root.state("zoomed")

        if not bool(self.current_user[5]):  # is_admin
            messagebox.showerror("Acesso Negado", "Apenas administradores podem acessar os relatórios de vendas.")
            self.root.destroy()
            return

        self.create_widgets()
        self.load_sales_reports()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(main_frame, text="Relatórios de Vendas por Vendedor", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Treeview para exibir os relatórios
        self.reports_tree = ttk.Treeview(main_frame, columns=("Vendedor", "Total Vendas (R$)", "Número de Vendas"), show="headings")
        self.reports_tree.heading("Vendedor", text="Vendedor")
        self.reports_tree.heading("Total Vendas (R$)", text="Total Vendas (R$)")
        self.reports_tree.heading("Número de Vendas", text="Número de Vendas")

        self.reports_tree.column("Vendedor", width=200)
        self.reports_tree.column("Total Vendas (R$)", width=150, anchor=tk.E)
        self.reports_tree.column("Número de Vendas", width=150, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.reports_tree.yview)
        self.reports_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.reports_tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Resumo geral
        ttk.Label(main_frame, text="Resumo Geral", font=("Helvetica", 14, "bold")).pack(pady=10)
        self.total_sales_label = ttk.Label(main_frame, text="Total Geral de Vendas: R$ 0.00", font=("Helvetica", 12))
        self.total_sales_label.pack(anchor=tk.W)
        self.total_items_sold_label = ttk.Label(main_frame, text="Total de Itens Vendidos: 0", font=("Helvetica", 12))
        self.total_items_sold_label.pack(anchor=tk.W)
        self.current_stock_value_label = ttk.Label(main_frame, text="Valor Atual do Estoque: R$ 0.00", font=("Helvetica", 12))
        self.current_stock_value_label.pack(anchor=tk.W)

    def load_sales_reports(self):
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)

        conn = create_connection()
        if conn is not None:
            sales_by_user = get_sales_by_user(conn)
            total_general_sales = 0.0
            total_general_items_sold = 0

            for user_id, total_sales, num_sales in sales_by_user:
                user_info = get_user_by_id(conn, user_id)
                seller_name = user_info[3] if user_info else "Desconhecido"
                self.reports_tree.insert("", tk.END, values=(
                    seller_name,
                    f"{total_sales:.2f}",
                    num_sales
                ))
                total_general_sales += total_sales

            # Calcular valor total do estoque
            all_products = get_all_products(conn)
            current_stock_value = 0.0
            for product in all_products:
                current_stock_value += product[4] * product[5]  # price * quantity
                # Adicionar lógica para total de itens vendidos se necessário
                # Isso exigiria uma query mais complexa para somar as quantidades de sale_items

            conn.close()

            self.total_sales_label.config(text=f"Total Geral de Vendas: R$ {total_general_sales:.2f}")
            # self.total_items_sold_label.config(text=f"Total de Itens Vendidos: {total_general_items_sold}") # Precisa de query específica
            self.current_stock_value_label.config(text=f"Valor Atual do Estoque: R$ {current_stock_value:.2f}")


