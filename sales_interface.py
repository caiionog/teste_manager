import tkinter as tk
from tkinter import ttk, messagebox
from database import create_connection, get_all_sales, delete_sale, get_user_by_id

class SalesManagementApp:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("Gerenciamento de Notas")
        self.root.state("zoomed")

        self.create_widgets()
        self.load_sales()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(main_frame, text="Notas Fiscais", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Treeview para exibir as notas
        self.sales_tree = ttk.Treeview(main_frame, columns=("ID", "Data", "Vendedor", "Cliente", "Total"), show="headings")
        self.sales_tree.heading("ID", text="ID")
        self.sales_tree.heading("Data", text="Data")
        self.sales_tree.heading("Vendedor", text="Vendedor")
        self.sales_tree.heading("Cliente", text="Cliente")
        self.sales_tree.heading("Total", text="Total (R$)")

        self.sales_tree.column("ID", width=50, anchor=tk.CENTER)
        self.sales_tree.column("Data", width=150, anchor=tk.CENTER)
        self.sales_tree.column("Vendedor", width=150)
        self.sales_tree.column("Cliente", width=200)
        self.sales_tree.column("Total", width=100, anchor=tk.E)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.sales_tree.yview)
        self.sales_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sales_tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Botões de ação
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        self.delete_button = ttk.Button(button_frame, text="Excluir Nota", command=self.delete_selected_sale)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Desabilitar botão de exclusão para usuários comuns
        if not bool(self.current_user[5]):  # is_admin
            self.delete_button.config(state=tk.DISABLED)

    def load_sales(self):
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)

        conn = create_connection()
        if conn is not None:
            sales = get_all_sales(conn)
            for sale in sales:
                # sale[8] é o user_id do vendedor
                seller_info = get_user_by_id(conn, sale[8])
                seller_name = seller_info[3] if seller_info else "Desconhecido"
                self.sales_tree.insert("", tk.END, values=(
                    sale[0],  # ID
                    sale[1],  # Data
                    seller_name, # Vendedor
                    sale[2],  # Cliente
                    f"{sale[6]:.2f}"  # Total
                ))
            conn.close()

    def delete_selected_sale(self):
        if not bool(self.current_user[5]):
            messagebox.showerror("Acesso Negado", "Apenas administradores podem excluir notas.")
            return

        selected_item = self.sales_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione uma nota para excluir.")
            return

        sale_id = self.sales_tree.item(selected_item[0], "values")[0]
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a nota fiscal ID {sale_id}?"):
            conn = create_connection()
            if conn is not None:
                if delete_sale(conn, sale_id):
                    messagebox.showinfo("Sucesso", "Nota fiscal excluída com sucesso!")
                    self.load_sales()
                else:
                    messagebox.showerror("Erro", "Não foi possível excluir a nota fiscal.")
                conn.close()


