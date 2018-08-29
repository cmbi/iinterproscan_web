
from flask import Blueprint, request
from flask.json import jsonify

from interproscan_web.controllers.job import (submit_if_needed,
                                              get_status,
                                              get_result)


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/submit/', methods=['POST'])
def submit():
    sequence = request.form.get('sequence', '')
    if len(sequence) <= 0:
        return jsonify({'error': "No sequence"}), 400

    job_id = submit_if_needed(sequence)
    return jsonify({'job_id': job_id})


@bp.route('/status/', methods=['GET'])
def status(job_id):
    status = get_status(job_id)
    return jsonify({'status': status})


@bp.route('/result/', methods=['GET'])
def result(job_id):
    try:
        result = get_result(job_id)
        return result
    except Exception as e:
        msg = str(e)
        return jsonify({'error': msg}), 500
