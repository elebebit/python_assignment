from flask import Blueprint, request
from sqlalchemy import text
from common import db
from datetime import datetime
import json

bp = Blueprint('statistics', __name__, url_prefix='/api')


@bp.route('/statistics', methods=['GET'])
def index():
    """
        statistics data api
    """
    content = []
    error_info = ''
    try:
        args = request.args
        symbol = args.get('symbol', '')
        start_date = args.get('start_date', '')
        end_date = args.get('end_date', '')

        if (datetime.strptime(start_date, '%Y-%m-%d') - datetime.strptime(end_date, '%Y-%m-%d')).days > 0:
            raise Exception('start_date is not before end_date!')

        if not all([symbol, start_date, end_date]):
            raise Exception("You have to put all the necessary parameters!")

        param_dict = {}
        conditions = ""
        if symbol:
            conditions += " and symbol = :symbol"
            param_dict['symbol'] = symbol
        if start_date:
            conditions += " and date >= :start_date"
            param_dict['start_date'] = start_date
        if end_date:
            conditions += " and date >= :end_date"
            param_dict['end_date'] = end_date
        sql = "select avg(open_price), avg(close_price), avg(volume)  from financial_data where 1=1 {};".format(
            conditions)
        items = db.session.execute(text(sql), param_dict).fetchall()

        for item in items:
            current_info = {"symbol": symbol,
                            "start_date": str(datetime.strptime(start_date, '%Y-%m-%d').date()),
                            "end_date": str(datetime.strptime(end_date, '%Y-%m-%d').date()),
                            "average_daily_open_price": str(round(item[0], 2)),
                            "average_daily_close_price": str(round(item[1], 2)),
                            "average_daily_volume": str(int(item[2]))}
            content.append(current_info)

        return json.dumps({"data": content, "info": {"error": error_info}})

    except Exception as e:
        return json.dumps({"data": content, "info": {"error": str(e)}})
