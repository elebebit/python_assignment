import os
from flask import Flask
from common import db
import pymysql
from dotenv import load_dotenv
import mysql.connector

basedir = os.path.abspath(os.path.dirname(__file__))

pymysql.install_as_MySQLdb()
load_dotenv()


def create_app():
    """
        Flask Factory App
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # register the financial data api
    from api import FinancialData
    app.register_blueprint(FinancialData.bp)

    # register the statistics data api
    from api import StatisticsData
    app.register_blueprint(StatisticsData.bp)

    return app


if __name__ == '__main__':
    app_ins = create_app()
    app_ins.run(debug=True, host='0.0.0.0',port=5000)
