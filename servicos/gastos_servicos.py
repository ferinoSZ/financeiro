from financia_db import mysql
from servicos.categorizador import categorizar
from datetime import datetime

def registrar_gasto(data):
    descricao = data.get('descricao')
    categoria = data.get('categoria') or categorizar(descricao)
    valor = data.get('valor')
    
    dia = data.get('dia')
    if not dia:
        dia = datetime.now().strftime('%Y-%m-%d')

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO financeiro.gastos (descricao, categoria, valor, dia) VALUES (%s, %s, %s, %s)", (descricao, categoria, valor, dia))
    mysql.connection.commit()
    cursor.close()

    return {"message": "Gasto registrado com sucesso!"}

def listar_gastos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM gastos")
    transacao = cursor.fetchall()
    cursor.close()

    return transacao

def filtro_por_data(data):
    day = data.get('dia')
    mes = data.get('mes')
    ano = data.get('ano')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM gastos WHERE (%s IS NULL OR YEAR(dia) = %s) AND (%s IS NULL OR MONTH(dia) = %s) AND (%s IS NULL OR DAY(dia) = %s)", (ano, ano, mes, mes, day, day))
    historico = cursor.fetchall()
    cursor.close()

    return historico

def filtro_por_categoria(data):
    categoria = data.get('categoria')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM gastos WHERE categoria = %s", (categoria,))
    historico = cursor.fetchall()
    cursor.close()

    return historico

def gerar_resumo_mensal(data):
    mes = data.get('mes')
    ano = data.get('ano')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT SUM(valor) FROM gastos WHERE YEAR(dia) = %s AND MONTH(dia) = %s", (ano, mes))
    resultado_total = cursor.fetchone()
    cursor.close()

    total = resultado_total[0] if resultado_total[0] else 0
    return {f"total do mês {mes}/{ano}": total}

def gerar_resumo_categoria(data):
    categoria = data.get('categoria')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT SUM(valor) FROM gastos WHERE categoria = %s", (categoria,))
    resultado_categoria = cursor.fetchone()
    cursor.close()

    total = resultado_categoria[0] if resultado_categoria[0] else 0
    return {"total": total}

def editar_gasto(id, data):
    descricao = data.get('descricao')
    categoria = data.get('categoria')
    valor = data.get('valor')

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE gastos SET descricao = %s, categoria = %s, valor = %s WHERE id = %s", (descricao, categoria, valor, id))
    mysql.connection.commit()
    cursor.close()

    return {"message": "Gasto atualizado com sucesso!"}