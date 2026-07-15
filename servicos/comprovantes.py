from doctr.io import DocumentFile
from doctr.models import ocr_predictor

foto = r"C:\Users\wesll\OneDrive\Documentos\estudos\Python\financeiro\servicos\img\teste_ocr.jpeg"

def extrair_texto_cupom(foto):
    print("Iniciando a leitura do cupom...")
    
    modelo = ocr_predictor(pretrained=True)
    documento = DocumentFile.from_images(foto)

    resultado = modelo(documento)

    texto_extraido = ""

    for pagina in resultado.pages:
        for bloco in pagina.blocks:
            for linha in bloco.lines:
                for palavra in linha.words:
                    texto_extraido += palavra.value + " "
                texto_extraido += "\n"

    return texto_extraido

texto = extrair_texto_cupom(foto)
print(texto)