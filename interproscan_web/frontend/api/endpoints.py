import xml.etree.ElementTree as ET
import logging
import traceback

from flask import Blueprint, request
from flask.json import jsonify

from interproscan_web.controllers.job import job_manager
from interproscan_web.controllers.sequence import is_sequence


bp = Blueprint('api', __name__, url_prefix='/api')


_log = logging.getLogger(__name__)


@bp.route('/run/', methods=['POST'], strict_slashes=False)
def run():
    _log.debug("run call")

    sequence = request.form.get('sequence', '')
    if len(sequence) <= 0:
        return _wrap_error("No sequence"), 400

    if not is_sequence(sequence):
        return _wrap_error("Invalid sequence"), 400

    return job_manager.submit(sequence)


@bp.route('/status/<job_id>/', methods=['GET'])
def status(job_id):
    status = job_manager.get_status(job_id)

    _log.debug("status for {} is {}".format(job_id, status))

    return status


@bp.route('/result/<job_id>/xml', methods=['GET'])
def result(job_id):
    try:
        result = job_manager.get_result(job_id)
        _log.debug("got result {}".format(result))
        return result
    except Exception as e:
        _log.error(traceback.format_exc())
        return _wrap_error(str(e)), 500


def _wrap_error(msg):
    err = ET.Element('error')
    desc = err = ET.Element('description')
    err.append(desc)
    desc.text = msg

    return ET.tostring(err)
