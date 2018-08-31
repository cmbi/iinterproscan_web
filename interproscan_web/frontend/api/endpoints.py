import xml.etree.ElementTree as ET
import logging

from flask import Blueprint, request
from flask.json import jsonify

from interproscan_web.controllers.job import job_manager


bp = Blueprint('api', __name__, url_prefix='/api')


_log = logging.getLogger(__name__)


@bp.route('/run/', methods=['POST'])
def run():
    _log.debug("run call")

    sequence = request.form.get('sequence', '')
    if len(sequence) <= 0:
        el = ET.Element('error')
        el.text = "No sequence"
        return ET.tostring(el), 400

    return job_manager.submit(sequence)


@bp.route('/status/<job_id>/', methods=['GET'])
def status(job_id):
    _log.debug("status call")

    return job_manager.get_status(job_id)


@bp.route('/result/<job_id>.xml', methods=['GET'])
def result(job_id):
    _log.debug("result call")

    try:
        result = job_manager.get_result(job_id)
        return result
    except Exception as e:
        el = ET.Element('error')
        el.text = str(e)
        return ET.tostring(el), 500
