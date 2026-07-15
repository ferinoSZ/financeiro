from flask import Blueprint, jsonify, request
from servicos import gastos_servicos

transacao_bp = Blueprint("transacao", __name__)

@transacao_bp.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    resultado = gastos_servicos.registrar_gasto(data)
    return jsonify(resultado), 201


@transacao_bp.route("/historico", methods=["GET"])
def historico():
    filtros = request.args.to_dict()

    resultado = gastos_servicos.buscar_gastos(filtros)
       
    return jsonify(resultado), 200

@transacao_bp.route("/resumo_mensal", methods=["GET"])
def resumo_mensal():
    data = request.args.to_dict()
    resultado = gastos_servicos.gerar_resumo_mensal(data)
    return jsonify(resultado), 200

@transacao_bp.route("/resumo_categoria", methods=["GET"])
def resumo_categoria():
    data = request.args.to_dict()
    resultado = gastos_servicos.gerar_resumo_categoria(data)
    return jsonify(resultado), 200

@transacao_bp.route("/editar_gasto/<int:id>", methods=["PUT"])
def editar(id):
    # PUT modifica dados, então mantém o get_json()
    data = request.get_json()
    resultado = gastos_servicos.editar_gasto(id, data)
    return jsonify(resultado), 200