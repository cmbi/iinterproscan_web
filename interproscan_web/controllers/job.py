import os
from bz2 import BZ2File

from celery.result import AsyncResult
from flask import current_app as app
from lockfile import LockFile

from interproscan_web.controllers.interproscan import interproscan
from interproscan_web.controllers.sequence import get_sequence_id
from interproscan_web.tasks import build_for



def get_result_path(sequence_id):
    return os.path.join(_get_dir_path_for(sequence_id), 'result.xml.bz2')


def _get_task_path(sequence_id):
    return os.path.join(_get_dir_path_for(sequence_id), 'celery_task')


def _get_dir_path_for(sequence_id):
    return os.path.join(app.config['DATADIR_PATH'], sequence_id)


def _get_lock_for(sequence_id):
    lock_dir_path = _get_dir_path_for(sequence_id)

    if not os.path.isdir(lock_dir_path):
        os.mkdir(lock_dir_path)

    return LockFile(lock_dir_path)


def submit_if_needed(sequence):
    sequence_id = get_sequence_id(sequence)

    output_path = get_result_path(sequence_id)
    task_path = _get_task_path(sequence_id)

    with _get_lock_for(sequence_id):
        from interproscan_web.tasks import build_for
        result = build_for.delay(sequence)

        with open(task_path, 'w') as f:
            f.write(result.task_id)
    return sequence_id


def get_status(sequence_id):
    result_path = get_result_path(sequence_id)

    with _get_lock_for(sequence_id):
        if os.path.isfile(result_path):
            return 'SUCCESS'

        if os.path.isfile(task_path):
            with open(task_path, 'r') as f:
                task_id = f.read()

            result = AsyncResult(task_id)
            return result.status
        else:
            return 'PENDING'


def get_result(sequence_id):
    result_path = get_result_path(sequence_id)

    with _get_lock_for(sequence_id):
        if os.path.isfile(result_path):
            with BZ2File(result_path, 'r') as f:
                return f.read()

        if os.path.isfile(task_path):
            with open(task_path, 'r') as f:
                task_id = f.read()

            result = AsyncResult(task_id)
            content = result.get()
            with BZ2File(result_path, 'w') as f:
                f.write(content)
            return content
        else:
            raise FileNotFoundError(task_path)
