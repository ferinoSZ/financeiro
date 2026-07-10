import chromadb
from chromadb.utils import embedding_functions
from gastos_servicos import registrar_gasto

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="colecao_db")

modelo_ia = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

if collection.count() == 0:
    print("Banco vazio! treiando IA pela primeira vez")
    collection.add(
        documents=[
            "supermercado, padaria, açougue, hortifruti, comida, lanche, ifood",
            "posto de gasolina, uber, 99, passagem de ônibus, mecânico",
            "farmácia, remédio, hospital, médico, dentista, consulta",
        ]
        metadatas=[
            {"categoria": "Alimentação"},
            {"categoria": "Transporte"},
            {"categoria": "Saúde"}
        ]
        ids=[
            "cat_1",
            "cat_2",
            "cat_3",
        ]
    )
    print("IA treinada com sucesso!!")

def categorizar(descricao):
    resultado = collection.query
    (
        query_texts=[descricao],
        n_results=1
    )
    try:
        categoria_sugerida = resultado['metadatas'[0][0]['catgoria']]
        return categoria_sugerida
    except:
        return "Outros"

# TESTE  
    
if __name__ == "main":
    print(\n "--- Testando a IA ---")
    print(f"Comprei pão -> {categorizar('Comprei pão')}")
    print(f"Abasteci o carro -> {categorizar('Abasteci o carro')}")
    print(f"Comprei um dramim na farmácia -> {categorizar('Comprei um dramim na farmácia')}")
    