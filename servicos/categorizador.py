import chromadb
from chromadb.utils import embedding_functions
chroma_client = chromadb.PersistentClient(path="./chroma_data")

modelo_ia = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
    )

collection = chroma_client.get_or_create_collection(
    name="colecao_db",
    embedding_function=modelo_ia
    )

dados_semente = {
    "Alimentação": "mercado, supermercado, restaurante, lanchonete, padaria, iFood, uber eats, rappy, almoço, janta, comprei pão, café da manhã, lanche, pizzaria, churrascaria, mcdonalds, burger king, feira, açougue, hortifruti",
    
    "Transporte": "combustível, posto de gasolina, abastecer, uber, 99app, ônibus, passagem, pedágio, estacionamento, metrô, trem, balsa, táxi, recarga de cartão de transporte",
    
    "Moradia": "aluguel, imobiliária, condomínio, IPTU, manutenção da casa, reforma, material de construção, encanador, eletricista, pintor, móveis, chaveiro, conserto, faxina, diarista",
    
    "Contas": "conta de água, sabesp, conta de luz, energia elétrica, conta de internet, wifi, telefone, plano de celular, gás de cozinha, gás encanado, boleto da luz, boleto da água",
    
    "Saúde": "farmácia, remédio, dorflex, dipirona, consulta médica, exames, laboratório, academia, mensalidade da academia, dentista, plano de saúde, psicólogo, terapia, hospital, clínica",
    
    "Educação": "faculdade, mensalidade escolar, universidade, cursos, udemy, alura, livros, material escolar, papelaria, mochila, caderno, xerox, curso de inglês, pós-graduação",
    
    "Lazer": "cinema, ingresso, jogos, videogame, playstation, steam, streaming, passeios, viagens curtas, museu, show, teatro, praia, barzinho, balada, cerveja com amigos, boliche",
    
    "Vestuário": "roupas, calçados, tênis, sapatos, acessórios, blusa, calça, casaco, camisa, loja de roupas, comprar casaco, relógio, óculos de sol, boné",
    
    "Compras": "eletrônicos, celular, computador, móveis, decoração, utensílios de cozinha, eletrodomésticos, geladeira, fogão, comprar tv, amazon compras, mercado livre, shopee",
    
    "Pets": "ração, pet shop, veterinário, consulta pet, banho e tosa, vacina cachorro, remédio gato, coleira, brinquedo pet, clínica veterinária",
    
    "Trabalho": "ferramentas, software, equipamentos, cursos profissionais, linkedin premium, hospedagem de site, domínio, notebook de trabalho, mouse, teclado, material de escritório",
    
    "Impostos e Taxas": "IPVA, imposto de renda, IR, multas de trânsito, tarifas bancárias, taxa de conta, anuidade, renovação de CNH, licenciamento, taxas do governo",
    
    "Dívidas": "empréstimos, financiamento de carro, financiamento de casa, pagamento de fatura, parcela do cartão de crédito, quitação de dívida, juros",
    
    "Presentes e Doações": "presentes, presente de aniversário, caridade, doação, contribuições, vaquinha, dízimo, oferta, flores, bombom de presente",
    
    "Viagens": "hotel, airbnb, hospedagem, passagens aéreas, decolar, passeios na viagem, aluguel de carro, mala de viagem, seguro viagem, viagem de férias",
    
    "Assinaturas": "netflix, spotify, ChatGPT, chatgpt plus, amazon prime, icloud, google one, disney plus, hbo max, youtube premium, crunchyroll",
    
    "Cuidados Pessoais": "barbeiro, barbearia, corte de cabelo, salão de beleza, cosméticos, maquiagem, perfume, desodorante, sabonete, shampoo, higiene pessoal, depilação",
    
    "Outros": "diversos, outros gastos, despesas gerais, tarifa desconhecida, pix enviado sem identificação"
}

lista_ids = []
lista_docs = []
lista_meta = []

cont = 1

for categoria, contexto in dados_semente.items():
    id_gerado = f"cat_{cont}"
    lista_ids.append(id_gerado)

    lista_docs.append(contexto)
    lista_meta.append({"categoria": categoria})

    cont +=1

if collection.count() == 0:
    print("Banco vazio! treiando IA pela primeira vez")
    collection.add(
        ids=lista_ids,
        documents=lista_docs,
        metadatas=lista_meta
    )
    print("IA treinada com sucesso!!")

def categorizar(descricao):
    resultado = collection.query(
        query_texts=[descricao],
        n_results=1
    )

    try:
        categoria_sugerida = resultado['metadatas'][0][0]['categoria']
        return categoria_sugerida
    except:
        return "Outros"

# TESTE  
    
if __name__ == "__main__":
    print("\n --- Testando a IA ---")
    print(f"Spotify -> {categorizar('Spotify')}")
    print(f"presente pro meu namorado -> {categorizar('presente pro meu namorado')}")
    print(f"boleto da formatura -> {categorizar('boleto da formatura')}")
    