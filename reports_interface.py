import tkinter as tk
from tkinter import ttk, messagebox
from database import create_connection, get_sales_by_user, get_all_products, get_user_by_id, get_all_sales
import statistics
from datetime import datetime, timedelta

class ReportsManagementApp:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("Relatórios de Vendas")
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
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(title_frame, text="Relatórios de Vendas por Vendedor", font=("Helvetica", 16, "bold")).pack(side=tk.LEFT)
        
        # Botão de Análise de IA
        ai_button = ttk.Button(title_frame, text="🤖 Análise de IA - Desempenho", 
                              command=self.generate_ai_performance_report,
                              style='Accent.TButton')
        ai_button.pack(side=tk.RIGHT, padx=10)

        # Treeview para exibir os relatórios
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.reports_tree = ttk.Treeview(tree_frame, columns=("Vendedor", "Total Vendas (R$)", "Número de Vendas", "Ticket Médio", "Status"), show="headings")
        self.reports_tree.heading("Vendedor", text="Vendedor")
        self.reports_tree.heading("Total Vendas (R$)", text="Total Vendas (R$)")
        self.reports_tree.heading("Número de Vendas", text="Número de Vendas")
        self.reports_tree.heading("Ticket Médio", text="Ticket Médio")
        self.reports_tree.heading("Status", text="Status Performance")

        self.reports_tree.column("Vendedor", width=150)
        self.reports_tree.column("Total Vendas (R$)", width=120, anchor=tk.E)
        self.reports_tree.column("Número de Vendas", width=120, anchor=tk.CENTER)
        self.reports_tree.column("Ticket Médio", width=100, anchor=tk.E)
        self.reports_tree.column("Status", width=150, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.reports_tree.yview)
        self.reports_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.reports_tree.pack(fill=tk.BOTH, expand=True)

        # Frame para resumo e análise
        summary_frame = ttk.LabelFrame(main_frame, text="Resumo Geral e Análise", padding="10")
        summary_frame.pack(fill=tk.X, pady=10)
        
        # Resumo geral
        left_summary = ttk.Frame(summary_frame)
        left_summary.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.total_sales_label = ttk.Label(left_summary, text="Total Geral de Vendas: R$ 0.00", font=("Helvetica", 12))
        self.total_sales_label.pack(anchor=tk.W)
        self.total_items_sold_label = ttk.Label(left_summary, text="Total de Itens Vendidos: 0", font=("Helvetica", 12))
        self.total_items_sold_label.pack(anchor=tk.W)
        self.current_stock_value_label = ttk.Label(left_summary, text="Valor Atual do Estoque: R$ 0.00", font=("Helvetica", 12))
        self.current_stock_value_label.pack(anchor=tk.W)
        
        # Análise rápida
        right_summary = ttk.Frame(summary_frame)
        right_summary.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.avg_ticket_label = ttk.Label(right_summary, text="Ticket Médio Geral: R$ 0.00", font=("Helvetica", 12))
        self.avg_ticket_label.pack(anchor=tk.W)
        self.best_seller_label = ttk.Label(right_summary, text="Melhor Vendedor: -", font=("Helvetica", 12))
        self.best_seller_label.pack(anchor=tk.W)
        self.performance_summary_label = ttk.Label(right_summary, text="Performance Geral: -", font=("Helvetica", 12))
        self.performance_summary_label.pack(anchor=tk.W)

    def load_sales_reports(self):
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)

        conn = create_connection()
        if conn is not None:
            sales_by_user = get_sales_by_user(conn)
            total_general_sales = 0.0
            total_general_items_sold = 0
            all_tickets = []
            user_performances = []

            for user_id, total_sales, num_sales in sales_by_user:
                user_info = get_user_by_id(conn, user_id)
                seller_name = user_info[3] if user_info else "Desconhecido"
                
                # Calcular ticket médio
                avg_ticket = total_sales / num_sales if num_sales > 0 else 0
                all_tickets.append(avg_ticket)
                
                # Determinar status de performance (análise básica)
                if num_sales >= 10 and avg_ticket >= 50:
                    status = "🟢 Excelente"
                elif num_sales >= 5 and avg_ticket >= 30:
                    status = "🟡 Bom"
                elif num_sales >= 3:
                    status = "🟠 Regular"
                else:
                    status = "🔴 Precisa Melhorar"
                
                user_performances.append({
                    'name': seller_name,
                    'total_sales': total_sales,
                    'num_sales': num_sales,
                    'avg_ticket': avg_ticket,
                    'status': status
                })
                
                self.reports_tree.insert("", tk.END, values=(
                    seller_name,
                    f"{total_sales:.2f}",
                    num_sales,
                    f"R$ {avg_ticket:.2f}",
                    status
                ))
                total_general_sales += total_sales

            # Calcular valor total do estoque
            all_products = get_all_products(conn)
            current_stock_value = 0.0
            for product in all_products:
                current_stock_value += product[4] * product[5]  # price * quantity

            # Calcular total de itens vendidos
            all_sales = get_all_sales(conn)
            total_general_items_sold = len(all_sales)

            conn.close()

            # Atualizar labels
            self.total_sales_label.config(text=f"Total Geral de Vendas: R$ {total_general_sales:.2f}")
            self.total_items_sold_label.config(text=f"Total de Vendas Realizadas: {total_general_items_sold}")
            self.current_stock_value_label.config(text=f"Valor Atual do Estoque: R$ {current_stock_value:.2f}")
            
            # Análise geral
            if all_tickets:
                general_avg_ticket = statistics.mean(all_tickets)
                self.avg_ticket_label.config(text=f"Ticket Médio Geral: R$ {general_avg_ticket:.2f}")
                
                # Melhor vendedor
                if user_performances:
                    best_seller = max(user_performances, key=lambda x: x['total_sales'])
                    self.best_seller_label.config(text=f"Melhor Vendedor: {best_seller['name']} (R$ {best_seller['total_sales']:.2f})")
                    
                    # Performance geral
                    excellent_count = sum(1 for p in user_performances if "Excelente" in p['status'])
                    total_sellers = len(user_performances)
                    if excellent_count / total_sellers >= 0.5:
                        performance_text = "🟢 Equipe com boa performance"
                    elif excellent_count / total_sellers >= 0.3:
                        performance_text = "🟡 Equipe com performance média"
                    else:
                        performance_text = "🔴 Equipe precisa de treinamento"
                    
                    self.performance_summary_label.config(text=f"Performance Geral: {performance_text}")

    def generate_ai_performance_report(self):
        """Gera relatório de análise de performance com IA"""
        try:
            # Coletar dados para análise
            conn = create_connection()
            if conn is None:
                messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados")
                return
            
            sales_by_user = get_sales_by_user(conn)
            all_sales = get_all_sales(conn)
            all_products = get_all_products(conn)
            
            # Análise de dados
            analysis_data = self.analyze_sales_data(sales_by_user, all_sales, all_products)
            
            # Gerar relatório com IA
            ai_report = self.generate_ai_insights(analysis_data)
            
            # Mostrar relatório em nova janela
            self.show_ai_report_window(ai_report)
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório de IA: {str(e)}")
    
    def analyze_sales_data(self, sales_by_user, all_sales, all_products):
        """Analisa os dados de vendas para gerar insights"""
        analysis = {
            'total_sellers': len(sales_by_user),
            'total_sales_value': sum(sale[1] for sale in sales_by_user),
            'total_transactions': sum(sale[2] for sale in sales_by_user),
            'sellers_performance': [],
            'stock_value': sum(product[4] * product[5] for product in all_products),
            'avg_transaction_value': 0,
            'performance_distribution': {'excellent': 0, 'good': 0, 'regular': 0, 'poor': 0}
        }
        
        if analysis['total_transactions'] > 0:
            analysis['avg_transaction_value'] = analysis['total_sales_value'] / analysis['total_transactions']
        
        # Analisar performance individual
        for user_id, total_sales, num_sales in sales_by_user:
            conn = create_connection()
            user_info = get_user_by_id(conn, user_id)
            conn.close()
            
            seller_name = user_info[3] if user_info else "Desconhecido"
            avg_ticket = total_sales / num_sales if num_sales > 0 else 0
            
            # Classificar performance
            if num_sales >= 10 and avg_ticket >= 50:
                performance_level = "excellent"
                analysis['performance_distribution']['excellent'] += 1
            elif num_sales >= 5 and avg_ticket >= 30:
                performance_level = "good"
                analysis['performance_distribution']['good'] += 1
            elif num_sales >= 3:
                performance_level = "regular"
                analysis['performance_distribution']['regular'] += 1
            else:
                performance_level = "poor"
                analysis['performance_distribution']['poor'] += 1
            
            analysis['sellers_performance'].append({
                'name': seller_name,
                'total_sales': total_sales,
                'num_sales': num_sales,
                'avg_ticket': avg_ticket,
                'performance_level': performance_level
            })
        
        return analysis
    
    def generate_ai_insights(self, data):
        """Gera insights usando lógica de IA baseada nos dados"""
        report = {
            'title': 'Relatório de Análise de Performance com IA',
            'summary': '',
            'recommendations': [],
            'critical_points': [],
            'strengths': [],
            'improvement_areas': []
        }
        
        # Análise geral
        total_sellers = data['total_sellers']
        excellent_ratio = data['performance_distribution']['excellent'] / total_sellers if total_sellers > 0 else 0
        poor_ratio = data['performance_distribution']['poor'] / total_sellers if total_sellers > 0 else 0
        
        # Gerar resumo
        if excellent_ratio >= 0.6:
            report['summary'] = f"🟢 EQUIPE DE ALTA PERFORMANCE: {excellent_ratio*100:.1f}% dos vendedores estão com performance excelente."
        elif excellent_ratio >= 0.3:
            report['summary'] = f"🟡 EQUIPE COM PERFORMANCE MÉDIA: {excellent_ratio*100:.1f}% dos vendedores estão com performance excelente."
        else:
            report['summary'] = f"🔴 EQUIPE PRECISA DE ATENÇÃO: Apenas {excellent_ratio*100:.1f}% dos vendedores estão com performance excelente."
        
        # Identificar pontos fortes
        if data['avg_transaction_value'] >= 100:
            report['strengths'].append("✅ Ticket médio alto indica boa capacidade de venda")
        
        if excellent_ratio >= 0.4:
            report['strengths'].append("✅ Boa proporção de vendedores com performance excelente")
        
        if data['total_transactions'] >= 50:
            report['strengths'].append("✅ Volume de vendas satisfatório")
        
        # Identificar áreas de melhoria
        if poor_ratio >= 0.3:
            report['improvement_areas'].append("⚠️ Alto número de vendedores com performance baixa")
        
        if data['avg_transaction_value'] < 50:
            report['improvement_areas'].append("⚠️ Ticket médio baixo - focar em vendas de maior valor")
        
        if data['total_transactions'] < 20:
            report['improvement_areas'].append("⚠️ Volume de vendas baixo - aumentar prospecção")
        
        # Pontos críticos
        poor_sellers = [s for s in data['sellers_performance'] if s['performance_level'] == 'poor']
        if poor_sellers:
            report['critical_points'].append(f"🚨 {len(poor_sellers)} vendedor(es) com performance crítica precisam de atenção imediata")
        
        low_ticket_sellers = [s for s in data['sellers_performance'] if s['avg_ticket'] < 30]
        if len(low_ticket_sellers) >= total_sellers * 0.5:
            report['critical_points'].append("🚨 Mais de 50% dos vendedores com ticket médio baixo")
        
        # Recomendações baseadas em IA
        if poor_ratio >= 0.3:
            report['recommendations'].append("🎯 TREINAMENTO URGENTE: Implementar programa de capacitação para vendedores com baixa performance")
        
        if data['avg_transaction_value'] < 50:
            report['recommendations'].append("🎯 ESTRATÉGIA DE UPSELLING: Treinar equipe em técnicas de venda cruzada e aumento de ticket")
        
        if excellent_ratio < 0.3:
            report['recommendations'].append("🎯 MENTORIA: Estabelecer programa de mentoria entre vendedores experientes e iniciantes")
        
        # Recomendações específicas por vendedor
        for seller in data['sellers_performance']:
            if seller['performance_level'] == 'poor':
                if seller['num_sales'] < 3:
                    report['recommendations'].append(f"🎯 {seller['name']}: Focar em aumento do volume de vendas (atual: {seller['num_sales']} vendas)")
                if seller['avg_ticket'] < 30:
                    report['recommendations'].append(f"🎯 {seller['name']}: Trabalhar técnicas de aumento de ticket médio (atual: R$ {seller['avg_ticket']:.2f})")
        
        # Identificar top performers para reconhecimento
        top_performers = [s for s in data['sellers_performance'] if s['performance_level'] == 'excellent']
        if top_performers:
            best_seller = max(top_performers, key=lambda x: x['total_sales'])
            report['strengths'].append(f"🏆 {best_seller['name']} é o destaque da equipe com R$ {best_seller['total_sales']:.2f} em vendas")
        
        return report
    
    def show_ai_report_window(self, report):
        """Mostra o relatório de IA em uma nova janela"""
        ai_window = tk.Toplevel(self.root)
        ai_window.title("Relatório de Análise de Performance com IA")
        ai_window.geometry("800x600")
        ai_window.resizable(True, True)
        
        # Frame principal com scrollbar
        main_frame = ttk.Frame(ai_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas e scrollbar
        canvas = tk.Canvas(main_frame, bg="white")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        title_label = ttk.Label(scrollable_frame, text=report['title'], font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Data do relatório
        date_label = ttk.Label(scrollable_frame, text=f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", font=("Arial", 10))
        date_label.pack(pady=5)
        
        # Resumo
        summary_frame = ttk.LabelFrame(scrollable_frame, text="📊 Resumo Executivo", padding="10")
        summary_frame.pack(fill=tk.X, pady=10)
        summary_label = ttk.Label(summary_frame, text=report['summary'], font=("Arial", 12, "bold"), wraplength=700)
        summary_label.pack()
        
        # Pontos Fortes
        if report['strengths']:
            strengths_frame = ttk.LabelFrame(scrollable_frame, text="💪 Pontos Fortes", padding="10")
            strengths_frame.pack(fill=tk.X, pady=10)
            for strength in report['strengths']:
                ttk.Label(strengths_frame, text=strength, font=("Arial", 10), wraplength=700).pack(anchor="w", pady=2)
        
        # Pontos Críticos
        if report['critical_points']:
            critical_frame = ttk.LabelFrame(scrollable_frame, text="🚨 Pontos Críticos", padding="10")
            critical_frame.pack(fill=tk.X, pady=10)
            for critical in report['critical_points']:
                ttk.Label(critical_frame, text=critical, font=("Arial", 10), wraplength=700, foreground="red").pack(anchor="w", pady=2)
        
        # Áreas de Melhoria
        if report['improvement_areas']:
            improvement_frame = ttk.LabelFrame(scrollable_frame, text="⚠️ Áreas de Melhoria", padding="10")
            improvement_frame.pack(fill=tk.X, pady=10)
            for improvement in report['improvement_areas']:
                ttk.Label(improvement_frame, text=improvement, font=("Arial", 10), wraplength=700, foreground="orange").pack(anchor="w", pady=2)
        
        # Recomendações
        if report['recommendations']:
            recommendations_frame = ttk.LabelFrame(scrollable_frame, text="🎯 Recomendações de IA", padding="10")
            recommendations_frame.pack(fill=tk.X, pady=10)
            for i, recommendation in enumerate(report['recommendations'], 1):
                ttk.Label(recommendations_frame, text=f"{i}. {recommendation}", font=("Arial", 10), wraplength=700).pack(anchor="w", pady=3)
        
        # Rodapé
        footer_frame = ttk.Frame(scrollable_frame)
        footer_frame.pack(fill=tk.X, pady=20)
        ttk.Label(footer_frame, text="Relatório gerado automaticamente pelo sistema de IA de análise de vendas", 
                 font=("Arial", 8, "italic")).pack()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botões
        button_frame = ttk.Frame(ai_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="💾 Salvar Relatório", command=lambda: self.save_ai_report(report)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🖨️ Imprimir", command=lambda: self.print_ai_report(report)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Fechar", command=ai_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def save_ai_report(self, report):
        """Salva o relatório de IA como arquivo de texto"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"Relatorio_IA_Performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"{report['title']}\n")
                    f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                    f.write("="*50 + "\n\n")
                    
                    f.write("RESUMO EXECUTIVO:\n")
                    f.write(f"{report['summary']}\n\n")
                    
                    if report['strengths']:
                        f.write("PONTOS FORTES:\n")
                        for strength in report['strengths']:
                            f.write(f"- {strength}\n")
                        f.write("\n")
                    
                    if report['critical_points']:
                        f.write("PONTOS CRÍTICOS:\n")
                        for critical in report['critical_points']:
                            f.write(f"- {critical}\n")
                        f.write("\n")
                    
                    if report['improvement_areas']:
                        f.write("ÁREAS DE MELHORIA:\n")
                        for improvement in report['improvement_areas']:
                            f.write(f"- {improvement}\n")
                        f.write("\n")
                    
                    if report['recommendations']:
                        f.write("RECOMENDAÇÕES DE IA:\n")
                        for i, recommendation in enumerate(report['recommendations'], 1):
                            f.write(f"{i}. {recommendation}\n")
                        f.write("\n")
                    
                    f.write("Relatório gerado automaticamente pelo sistema de IA de análise de vendas")
                
                messagebox.showinfo("Sucesso", f"Relatório salvo como: {filename}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar relatório: {str(e)}")
    
    def print_ai_report(self, report):
        """Imprime o relatório de IA"""
        messagebox.showinfo("Impressão", "Funcionalidade de impressão do relatório de IA será implementada em versão futura")

