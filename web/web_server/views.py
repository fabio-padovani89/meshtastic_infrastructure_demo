from datetime import datetime
from flask import jsonify, request
from web_server import app

from .db_interface import get_nodes_info

def resp(body, status=200):
    return (jsonify(body) if body else jsonify({})), status


def err_resp(body, status=422):
    return resp(body, status)


@app.route('/nodes/')
def nodes():
    # filters to be applied
    filters = {}

    # apply datetime filters
    dt_filters = (
        ('dt_from', 'dt-from'),
        ('dt_to', 'dt-to'),
    )
    for filt in dt_filters:
        key = filt[0]
        val = request.args.get(filt[1])
        if not val:
            continue
        try:
            filters[key] = datetime.fromisoformat(val)
        except ValueError:
            return err_resp({key: 'invalid'})

    # apply string filters
    str_filters = (
        ('user', 'user'),
    )
    for filt in str_filters:
        key = filt[0]
        val = request.args.get(filt[1])
        if val:
            filters[key] = val

    data = get_nodes_info(**filters)
    return resp(data)
