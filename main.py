import tkinter as tk
from tkinter import ttk
import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('financas.db')
c = conn.cursor()

# Criar tabela de despesas se não existir
c.execute('''CREATE TABLE IF NOT EXISTS despesas
             (id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, valor REAL)''')
conn.commit()

# Função para adicionar despesa ao banco de dados
def adicionar_despesa():
    categoria = combo_categoria.get()
    valor = float(entry_valor.get())
    c.execute("INSERT INTO despesas (categoria, valor) VALUES (?, ?)", (categoria, valor))
    conn.commit()
    entry_valor.delete(0, tk.END)
    mostrar_resumo()

# Função para mostrar resumo das despesas
def mostrar_resumo():
    for row in tree.get_children():
        tree.delete(row)
    c.execute("SELECT categoria, SUM(valor) FROM despesas GROUP BY categoria")
    for row in c.fetchall():
        tree.insert("", tk.END, values=row)
    c.execute("SELECT SUM(valor) FROM despesas")
    total_gastos = c.fetchone()[0]
    if total_gastos is None:
        total_gastos = 0
    lbl_total_gastos.config(text="Total de Gastos Mensais: R$ {:.2f}".format(total_gastos))

# Função para excluir despesa selecionada
def excluir_despesa():
    item_selecionado = tree.selection()
    if item_selecionado:
        item = tree.item(item_selecionado[0])
        categoria = item['values'][0]
        c.execute("DELETE FROM despesas WHERE categoria=?", (categoria,))
        conn.commit()
        mostrar_resumo()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Gerenciamento Financeiro Pessoal")

# Frame para entrada de despesas
frame_despesas = ttk.Frame(root)
frame_despesas.pack(padx=10, pady=10)

# Combobox para seleção da categoria da despesa
ttk.Label(frame_despesas, text="Categoria:").grid(row=0, column=0)
categorias = ['Alimentação', 'Transporte', 'Moradia', 'Lazer', 'Outros']
combo_categoria = ttk.Combobox(frame_despesas, values=categorias)
combo_categoria.grid(row=0, column=1, padx=5, pady=5)

# Entry para inserção do valor da despesa
ttk.Label(frame_despesas, text="Valor:").grid(row=1, column=0)
entry_valor = ttk.Entry(frame_despesas)
entry_valor.grid(row=1, column=1, padx=5, pady=5)

# Botão para adicionar despesa
btn_adicionar = ttk.Button(frame_despesas, text="Adicionar Despesa", command=adicionar_despesa)
btn_adicionar.grid(row=2, columnspan=2, pady=10)

# Frame para exibição do resumo das despesas
frame_resumo = ttk.Frame(root)
frame_resumo.pack(padx=10, pady=10)

# Treeview para exibir o resumo das despesas
tree = ttk.Treeview(frame_resumo, columns=("Categoria", "Total"), show="headings")
tree.heading("Categoria", text="Categoria")
tree.heading("Total", text="Total")
tree.pack()

# Botão para excluir despesa selecionada
btn_excluir = ttk.Button(root, text="Excluir Despesa Selecionada", command=excluir_despesa)
btn_excluir.pack(pady=10)

# Label para exibir o total de gastos mensais
lbl_total_gastos = ttk.Label(root, text="Total de Gastos Mensais: R$ 0.00")
lbl_total_gastos.pack()

# Mostrar resumo inicial
mostrar_resumo()

root.mainloop()
