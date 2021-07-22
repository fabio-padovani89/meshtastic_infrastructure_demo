from flask import jsonify, send_from_directory
from web_server import app

from .db_interface import get_nodes_info


@app.route('/nodes/')
def nodes():
    data = get_nodes_info()
    return jsonify(data)
