from flask import Blueprint, request
from sqlalchemy import text
from common import db
import math
import json

bp = Blueprint('financial_data', __name__, url_prefix='/api')


@bp.route('/financial_data', methods=['GET'])
def index():
    """
        financial data api
    """
    page_content = []
    error_info = ''
    try:
        args = request.args
        symbol = args.get('symbol', '')
        start_date = args.get('start_date', '')
        end_date = args.get('end_date', '')
        limit = int(args.get('limit', 5))
        page = int(args.get('page', 1))

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
        sql = "select * from financial_data where 1=1 {};".format(conditions)
        items = db.session.execute(text(sql), param_dict).fetchall()

        records = len(items)
        # judge the page index
        max_pages = math.ceil(records / limit)
        if page > max_pages:
            raise Exception("The current query exceeds the maximum page limit !")

        # get target content for the page
        page_items = get_page_content(items, page, limit)

        for item in page_items:
            current_info = {"symbol": item[1], "date": item[2].strftime('%Y-%m-%d'), "open_price": str(item[3]), "close_price": str(item[4]), "volume": item[5]}
            page_content.append(current_info)

        page_info = {"count": records, "page": page, "limit": limit, "pages": max_pages}
        return json.dumps({"data": page_content, "pagination": page_info, "info": {"error": error_info}})

    except Exception as e:
        return json.dumps({"info":{"error":str(e)}})


def get_page_content(query_list, page, page_limit):
    """
        get the page's content from all contents
    """
    start_index = (page - 1) * page_limit
    end_index = start_index + page_limit
    return query_list[start_index:end_index]


