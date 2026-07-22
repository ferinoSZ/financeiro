import telebot
import os
from dotenv import load_dotenv
from servicos import gastos_servicos

load_dotenv

token = os.getenv("token_telegram")
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['historico'])
def pegar_historico(message):
    try:
        texto = message.text
        palavras = texto.split()
        categoria_filtrada = None

        if len(palavras) > 1:
            categoria_filtrada = palavras[1]
        dados = gastos_servicos.obter_historico(categoria_filtrada)
        if not dados:
            bot.reply_to(message, "Não há nada no histórico, histórico vazio...!!!")
            return
        
        mensagem_final = "📊 **Últimos Lançamentos:**\n\n"
        for item in dados:
            detalhe = "🟢" if item['tipo'] == "ENTRADA" else "🔴"
            valor_americano = f"{item['valor']:,.2f}"
            valor_formatado = valor_americano.replace(".", "X").replace(",", ".").replace("X", ",")

            data_formatada = item['dia'].strftime('%d/%m/%Y') if item['dia'] else "S/D"
            mensagem_final += f"{detalhe} *{item['descricao']}* - R${valor_formatado} ({item['categoria']} em {data_formatada})\n\n\n"
        bot.reply_to(message, mensagem_final, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"Ih, deu erro no Python: {str(e)}", parse_mode="Markdown")

@bot.message_handler(commands=['ola'])
def saudacao(message):
    nome = message.from_user.first_name
    bot.reply_to(message, f"Olá, {nome}! Seja bem-vindo!")

@bot.message_handler(func=lambda message: True)
def ecoar_texto(message):
    ligacoes = ["da", "de", "do", "das", "dos", "em", "por"]

    texto = message.text
    palavras = texto.split()
    valor_final = palavras[-1]
    if palavras[-2] in ligacoes:
        resto_palavra = palavras[:-2]
    else:
        resto_palavra = palavras[:-1]
    descricao = " ".join(resto_palavra)

    try:
        if "," in valor_final:
            valor_limpo = valor_final.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
        else:
            valor_limpo = valor_final
        valor = float(valor_limpo)
        if valor <= 0:
            bot.reply_to(message, "O valor precisa ser maior que zero, por favor tente novamente.")
            return
    except ValueError:
        bot.reply_to(message, "Não consegui entender o valor, tem certeza que escreveu no final da frase?")
        return

    data = {
        "descricao": descricao,
        "valor": valor
    }

    resultado = gastos_servicos.registrar_gasto(data)

    if "error" in resultado:
        bot.reply_to(message, "Ops, ocorreu algum erro ao enviar para o banco de dados!!!")
    else:
        bot.reply_to(message, "Informação salva com sucesso no banco de dados!!!")

print("Bot treinado com sucesso!!")
bot.infinity_polling()