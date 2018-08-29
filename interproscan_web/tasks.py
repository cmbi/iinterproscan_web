import tempfile
import os

from celery import current_app as celery_app

from interproscan_web.controllers.sequence import get_sequence_id
from interproscan_web.controllers.interproscan import interproscan


@celery_app.task()
def build_for(sequence):
    xml_path = tempfile.mktemp()
    try:
        interproscan.run(sequence, xml_path)
        with open(xml_path, 'r') as f:
            return f.read()
    finally:
        if os.path.isfile(xml_path):
            os.remove(xml_path)
