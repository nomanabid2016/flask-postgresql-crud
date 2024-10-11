from http import HTTPStatus
from flask import jsonify
from .constants import ResponseBody, Status

# Utility functions for handling responses
def success_response(data=None, message=None, status=Status.SUCCESS):
    return jsonify({
        ResponseBody.STATUS: status,
        ResponseBody.DATA: data,
        ResponseBody.MESSAGE: message,
    })

def error_response(error_message, status_code=HTTPStatus.INTERNAL_SERVER_ERROR):
    return jsonify({
        ResponseBody.STATUS: Status.ERROR,
        ResponseBody.ERROR: error_message,
    }), 