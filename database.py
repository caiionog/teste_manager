import sqlite3
from sqlite3 import Error

def create_connection():
    """Cria uma conexão com o banco de dados SQLite"""
    conn = None
    try:
        conn = sqlite3.connect('users.db')
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    """Cria a tabela de usuários se não existir"""
    try:
        sql = '''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT,
                    is_admin INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );'''
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except Error as e:
        print(e)

def create_product_table(conn):
    """Cria a tabela de produtos se não existir"""
    try:
        sql = '''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    category TEXT,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    min_quantity INTEGER DEFAULT 0,
                    supplier TEXT,
                    barcode TEXT UNIQUE,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                );'''
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except Error as e:
        print(e)

def create_sales_tables(conn):
    """Cria as tabelas para vendas e itens de venda"""
    try:
        # Tabela de vendas
        sales_table = '''CREATE TABLE IF NOT EXISTS sales (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            sale_date TEXT DEFAULT CURRENT_TIMESTAMP,
                            customer_name TEXT,
                            customer_doc TEXT,
                            subtotal REAL NOT NULL,
                            discount REAL DEFAULT 0,
                            total REAL NOT NULL,
                            payment_method TEXT,
                            user_id INTEGER NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        );'''
        
        # Tabela de itens de venda
        sale_items_table = '''CREATE TABLE IF NOT EXISTS sale_items (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                sale_id INTEGER NOT NULL,
                                product_id INTEGER NOT NULL,
                                quantity INTEGER NOT NULL,
                                unit_price REAL NOT NULL,
                                total_price REAL NOT NULL,
                                FOREIGN KEY (sale_id) REFERENCES sales (id),
                                FOREIGN KEY (product_id) REFERENCES products (id)
                            );'''
        
        cursor = conn.cursor()
        cursor.execute(sales_table)
        cursor.execute(sale_items_table)
        conn.commit()
    except Error as e:
        print(e)

def create_client_table(conn):
    """Cria a tabela de clientes se não existir"""
    try:
        sql = '''CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    doc TEXT UNIQUE,
                    phone TEXT,
                    email TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );'''
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except Error as e:
        print(e)

def initialize_database():
    """Inicializa o banco de dados e cria tabelas necessárias"""
    conn = create_connection()
    if conn is not None:
        create_table(conn)          # Tabela de usuários
        create_product_table(conn)  # Tabela de produtos
        create_sales_tables(conn)   # Tabelas de vendas
        create_client_table(conn)   # Tabela de clientes
        
        # Verifica se existe algum admin
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin=1")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Cria um admin padrão (usuário: admin, senha: admin123)
            add_user(conn, "admin", "admin123", "Administrador", "admin@system.com", 1)
        
        conn.close()

def add_user(conn, username, password, full_name, email, is_admin=0):
    """Adiciona um novo usuário ao banco de dados"""
    try:
        sql = '''INSERT INTO users(username, password, full_name, email, is_admin)
                 VALUES(?,?,?,?,?)'''
        cursor = conn.cursor()
        cursor.execute(sql, (username, password, full_name, email, is_admin))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)
        return None

def get_all_users(conn):
    """Retorna todos os usuários do banco de dados"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    except Error as e:
        print(e)
        return []

def get_user_by_id(conn, user_id):
    """Retorna um usuário específico pelo ID"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        return cursor.fetchone()
    except Error as e:
        print(e)
        return None

def update_user(conn, user_id, username, password, full_name, email, is_admin):
    """Atualiza os dados de um usuário"""
    try:
        sql = '''UPDATE users
                 SET username=?, password=?, full_name=?, email=?, is_admin=?
                 WHERE id=?'''
        cursor = conn.cursor()
        cursor.execute(sql, (username, password, full_name, email, is_admin, user_id))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

def delete_user(conn, user_id):
    """Remove um usuário do banco de dados"""
    try:
        sql = 'DELETE FROM users WHERE id=?'
        cursor = conn.cursor()
        cursor.execute(sql, (user_id,))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

def login_user(conn, username, password):
    """Verifica as credenciais do usuário"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return cursor.fetchone()
    except Error as e:
        print(e)
        return None
    
def add_product(conn, name, description, category, price, quantity, min_quantity, supplier, barcode):
    """Adiciona um novo produto ao banco de dados"""
    try:
        sql = '''INSERT INTO products(name, description, category, price, quantity, min_quantity, supplier, barcode)
                 VALUES(?,?,?,?,?,?,?,?)'''
        cursor = conn.cursor()
        cursor.execute(sql, (name, description, category, price, quantity, min_quantity, supplier, barcode))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)
        return None

def get_all_products(conn):
    """Retorna todos os produtos do banco de dados"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()
    except Error as e:
        print(e)
        return []

def get_product_by_id(conn, product_id):
    """Retorna um produto específico pelo ID"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
        return cursor.fetchone()
    except Error as e:
        print(e)
        return None

def update_product(conn, product_id, name, description, category, price, quantity, min_quantity, supplier, barcode):
    """Atualiza os dados de um produto"""
    try:
        sql = '''UPDATE products
                 SET name=?, description=?, category=?, price=?, quantity=?, min_quantity=?, supplier=?, barcode=?, updated_at=CURRENT_TIMESTAMP
                 WHERE id=?'''
        cursor = conn.cursor()
        cursor.execute(sql, (name, description, category, price, quantity, min_quantity, supplier, barcode, product_id))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

def delete_product(conn, product_id):
    """Remove um produto do banco de dados"""
    try:
        sql = 'DELETE FROM products WHERE id=?'
        cursor = conn.cursor()
        cursor.execute(sql, (product_id,))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

def search_products(conn, search_term):
    """Busca produtos por nome, descrição ou categoria"""
    try:
        cursor = conn.cursor()
        search_term = f"%{search_term}%"
        cursor.execute("""
            SELECT * FROM products 
            WHERE name LIKE ? OR description LIKE ? OR category LIKE ? OR barcode LIKE ?
        """, (search_term, search_term, search_term, search_term))
        return cursor.fetchall()
    except Error as e:
        print(e)
        return []
    
def add_sale(conn, customer_name, customer_doc, subtotal, discount, total, payment_method, user_id):
    """Adiciona uma nova venda ao banco de dados"""
    try:
        sql = '''INSERT INTO sales(customer_name, customer_doc, subtotal, discount, total, payment_method, user_id)
                 VALUES(?,?,?,?,?,?,?)'''
        cursor = conn.cursor()
        cursor.execute(sql, (customer_name, customer_doc, subtotal, discount, total, payment_method, user_id))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)
        return None

def add_sale_item(conn, sale_id, product_id, quantity, unit_price, total_price):
    """Adiciona um item à venda"""
    try:
        sql = '''INSERT INTO sale_items(sale_id, product_id, quantity, unit_price, total_price)
                 VALUES(?,?,?,?,?)'''
        cursor = conn.cursor()
        cursor.execute(sql, (sale_id, product_id, quantity, unit_price, total_price))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)
        return None

def get_sale_by_id(conn, sale_id):
    """Obtém os detalhes de uma venda"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales WHERE id=?", (sale_id,))
        sale = cursor.fetchone()
        
        if sale:
            cursor.execute("""
                SELECT si.*, p.name 
                FROM sale_items si
                JOIN products p ON si.product_id = p.id
                WHERE si.sale_id=?
            """, (sale_id,))
            items = cursor.fetchall()
            return sale, items
        return None, None
    except Error as e:
        print(e)
        return None, None

def get_all_sales(conn):
    """Obtém todas as vendas"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, u.full_name 
            FROM sales s
            JOIN users u ON s.user_id = u.id
            ORDER BY s.sale_date DESC
        """
        )
        return cursor.fetchall()
    except Error as e:
        print(e)
        return []

def delete_sale(conn, sale_id):
    """Remove uma venda e seus itens do banco de dados"""
    try:
        cursor = conn.cursor()
        conn.execute("BEGIN TRANSACTION")
        cursor.execute("DELETE FROM sale_items WHERE sale_id=?", (sale_id,))
        cursor.execute("DELETE FROM sales WHERE id=?", (sale_id,))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        print(e)
        return False

def update_product_quantity(conn, product_id, quantity_sold):
    """Atualiza a quantidade em estoque de um produto"""
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET quantity = quantity - ? WHERE id=?", (quantity_sold, product_id))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

def add_client(conn, name, doc, phone, email):
    """Adiciona um novo cliente ao banco de dados"""
    try:
        sql = '''INSERT INTO clients(name, doc, phone, email)
                 VALUES(?,?,?,?)'''
        cursor = conn.cursor()
        cursor.execute(sql, (name, doc, phone, email))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)
        return None

def get_all_clients(conn):
    """Retorna todos os clientes do banco de dados"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        return cursor.fetchall()
    except Error as e:
        print(e)
        return []

def get_sales_by_user(conn):
    """Obtém o total de vendas e o número de vendas por usuário"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, SUM(total), COUNT(id)
            FROM sales
            GROUP BY user_id
        """
        )
        return cursor.fetchall()
    except Error as e:
        print(e)
        return []

