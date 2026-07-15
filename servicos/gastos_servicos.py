from financia_db import pegar_conexao
from servicos.categorizador import categorizar
from datetime import datetime

def registrar_gasto(data):
    descricao = data.get('descricao')
    valor = data.get('valor')

    if not descricao or not valor:
        return {"error": "Descrição e valor são obrigatórios."}, 400

    categoria = data.get('categoria') or categorizar(descricao)

    tipo = "ENTRADA" if categoria == "Receitas" else "SAIDA"
    
    dia = data.get('dia')
    if not dia:
        dia = datetime.now().strftime('%Y-%m-%d')

    conexao = None
    cursor = None
    try:
        conexao = pegar_conexao()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO financeiro.gastos (descricao, categoria, valor, dia, tipo) VALUES (%s, %s, %s, %s, %s)", (descricao, categoria, valor, dia, tipo))
        conexao.commit()

    except Exception as erro:
        return({"error": f"Erro no bando de dados: {str(erro)}"}, 500)
    finally:
        if cursor is not None:
            cursor.close()
        if conexao is not None:
            conexao.close()

    return {"message": "Gasto registrado com sucesso!"}

def obter_historico(categoria=None):
    query = """
        SELECT descricao, valor, categoria, tipo, dia 
        FROM financeiro.gastos
    """
    valores_query = []

    if categoria:
        query += " WHERE categoria = %s"
        valores_query.append(categoria)

    else:
        query += " ORDER BY id DESC LIMIT 10"
    try:
        conexao = pegar_conexao()
        cursor = conexao.cursor()
        if valores_query:
            cursor.execute(query, valores_query)
        else:
            cursor.execute(query)
        resultados = cursor.fetchall()

        return resultados
    except Exception as erro:
        print(f"Erro ao buscar histórico: {erro}")
        return[]
    finally:
        if cursor is not None:
            cursor.close()
        if conexao is not None:
            conexao.close()

def buscar_gastos(filtros):
    query = "SELECT * FROM financeiro.gastos WHERE 1=1"
    valores = []

    if 'categoria' in filtros:
        query += " AND categoria = %s"
        valores.append(filtros['categoria'])

    if 'data' in filtros:
        query += " AND dia = %s"
        valores.append(filtros['data'])

    if 'mes' in filtros:
        query += " AND MONTH(dia) = %s"
        valores.append(filtros['mes'])
        
    if 'tipo' in filtros:
        query += " AND tipo = %s"
        valores.append(filtros['tipo'])

    query += " ORDER BY dia DESC"

    try:
        cursor = mysql.connection.cursor()
        # Transformamos a nossa lista de valores em uma tupla para o MySQL
        cursor.execute(query, tuple(valores))
        
        colunas = [col[0] for col in cursor.description]
        resultados = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
        
        return resultados
    except Exception as e:
        return {"error": f"Erro na busca dinâmica: {str(e)}"}, 500
    finally:
        cursor.close()

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