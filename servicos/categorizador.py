def categorizar(descricao):
    if descricao == "Posto shell":
        categoria = "Transporte"
    elif descricao == "Mercado":
        categoria = "Alimentação"
    else:
        categoria = "Outros"
    return categoria
