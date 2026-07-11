dados_semente = {
    "Alimentação": "supermercado, mercado, padaria, açougue, hortifruti, comida, lanche, ifood, restaurante, delivery, pizza, hambúrguer, café, feira, pastel, pão, bolo, salgado",
    "Transporte": "posto de gasolina, combustível, abastecimento, uber, 99, passagem de ônibus, mecânico, oficina, estacionamento, pedágio, ipva, metrô, trem, pneu",
    "Saúde": "farmácia, remédio, hospital, médico, dentista, consulta, exame, plano de saúde, terapia, psicólogo, academia, dramin, dipirona",
    "Moradia": "aluguel, condomínio, conta de luz, energia, conta de água, internet, iptu, reforma, material de construção, móveis, encanador, eletricista",
    "Lazer": "cinema, netflix, spotify, show, jogo, viagem, ingresso, barzinho, balada, festa, streaming",
    "Educação": "faculdade, mensalidade escolar, curso, livro, papelaria, inglês, material escolar",
    "Despesas Pessoais": "roupa, calçado, salão de beleza, cabeleireiro, barbearia, cosmético, maquiagem, presente, pet shop, ração, veterinário"
}

lista_ids = []
lista_docs = []
lista_meta = []

cont = 1

for categoria, contexto in dados_semente.items():
    id_gerado = f"cat_{cont}"
    lista_ids.append(id_gerado)

    lista_docs.append(contexto)
    lista_meta.append({"Categoria": categoria})

    cont +=1

print(lista_ids)
print(lista_docs)
print(lista_meta)
    
