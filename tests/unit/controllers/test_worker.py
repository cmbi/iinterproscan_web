from time import sleep

from mock import patch
from nose.tools import ok_

from interproscan_web.controllers.worker import Worker
from interproscan_web.controllers.sequence import get_sequence_id


@patch("interproscan_web.controllers.interproscan.interproscan.run")
def test_result(mock_run):
    sequence = "TRY"
    sequence_id = get_sequence_id(sequence)

    mock_run.return_value = {sequence_id: 'OK'}

    worker = Worker()
    worker.submit(sequence)

    ok_(worker.has_sequence_id(sequence_id))

    worker.start()
    sleep(1.0)

    ok_(worker.result_for_sequence_id(sequence_id) is not None)
