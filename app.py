from dotenv import load_dotenv

from flask import Flask
from flask_mysqldb import MySQL
from financia_db import mysql
from rotas.transacao import transacao_bp

app = Flask(__name__)

load_dotenv()

mysql.init_app(app)


app.register_blueprint(transacao_bp)


if __name__ == "__main__":
	app.run(debug=True)
