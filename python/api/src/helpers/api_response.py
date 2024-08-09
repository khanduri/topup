from flask import jsonify
from src.helpers.ids import request_id

from datetime import datetime


def _pack_response(data, meta=None, response_code=200):
    meta_info = meta if meta else {}
    meta_info.update({
        'generated_at_utc': datetime.utcnow(),
        'request_id': request_id()
    })

    packed_data = {
        'data': data,
        'meta': meta_info,
    }
    return jsonify(packed_data), response_code


def return_packet_fail(reason, message=None, response_code=403):
    meta = {'success': False, }
    response = {
        'code': reason.value,
        'message': reason.message(child_message=message),
    }
    return _pack_response(response, meta=meta, response_code=response_code)


def return_packet_success(data=None, response_code=200):
    meta = {'success': True}
    data = data if data else {}
    return _pack_response(data, meta=meta, response_code=response_code)
