import tkinter as tk
from database import initialize_database
from user_interface import LoginWindow
from menu_interface import MainMenu
from ttkthemes import ThemedTk

def main():
    # Inicializar o banco de dados
    initialize_database()
    
    # Criar a janela principal de login
    root = ThemedTk()
    root.set_theme("black") # Define o tema escuro
    
    def on_login_success(user):
        # Quando o login é bem-sucedido, criar o menu principal
        app_root = ThemedTk()
        app_root.set_theme("black") # Define o tema escuro
        app = MainMenu(app_root, user)
        app_root.mainloop()
    
    login_app = LoginWindow(root, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()