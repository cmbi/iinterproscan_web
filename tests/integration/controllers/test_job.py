import tempfile
import os
import shutil

from nose.tools import with_setup, ok_, eq_
from mock import patch

from interproscan_web.controllers.sequence import get_sequence_id
from interproscan_web.controllers.job import job_manager
from interproscan_web.controllers.worker import Worker


def setup():
    job_manager.data_dir = tempfile.mkdtemp()
    job_manager.worker = Worker()
    job_manager.worker.start()


def teardown():
    if os.path.isdir(job_manager.data_dir):
        shutil.rmtree(job_manager.data_dir)


@with_setup(setup, teardown)
@patch("interproscan_web.controllers.interproscan.interproscan.run")
def test_job(mock_interproscan):
    sequence = "TRY"
    sequence_id = get_sequence_id(sequence)

    mock_interproscan.return_value = {sequence_id: "OK"}

    job_id = job_manager.submit(sequence)
    eq_(job_id, sequence_id)

    while True:
        status = job_manager.get_status(job_id)

        if status == 'SUCCESS':
            result = job_manager.get_result(job_id)
            ok_(result is not None)
            return

        ok_(status in ['PENDING', 'STARTED'])
