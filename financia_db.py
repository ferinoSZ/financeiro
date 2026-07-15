import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def pegar_conexao():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
        port=int(os.getenv("MYSQL_PORT", 3306)), # Porta precisa ser um número inteiro!
        cursorclass=pymysql.cursors.DictCursor
    )