from datetime import datetime
from urllib.parse import unquote
from flask import jsonify, request
from web_server import app

from .db_interface import get_nodes_info, get_node_path

def resp(body, status=200):
    return jsonify(body), status


def err_resp(body, status=422):
    return resp(body, status)


@app.route('/api/v1/nodes/')
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
            filters[key] = datetime.fromisoformat(unquote(val))
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
            filters[key] = unquote(val)

    data = get_nodes_info(**filters)
    return resp(data)

@app.route('/api/v1/nodes/<user>/path/')
def node_path(user):
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
            filters[key] = datetime.fromisoformat(unquote(val))
        except ValueError:
            return err_resp({key: 'invalid'})

    data = get_node_path(user, **filters)
    return resp(data)
