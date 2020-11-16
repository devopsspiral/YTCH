# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import requests
import uuid
from ansible.plugins.callback import CallbackBase
from ansible import constants as C


DOCUMENTATION = '''
    name: fluentd
    type: notification
    short_description: callback communicating with fluentd in_http plugin
    version_added: historical
    description:
      - This is plugin that allows sending ansible events to centralised logging systems using fluentd
'''

fluentd_url = "http://localhost/ansible.log"


class CallbackModule(CallbackBase):

    '''
    This is plugin that allows sending ansible events to
    centralised logging systems using fluentd.
    '''

    CALLBACK_VERSION = 1.0
    CALLBACK_NAME = 'fluentd'

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.main_playbook = None
        self.execution_id = None

    def _log(self, entry):
        requests.post(fluentd_url, json=entry)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        task = result._task.get_name()
        self._log({"host": host,
                   "task": task,
                   "result": result._result,
                   "playbook": self.main_playbook,
                   "id": self.execution_id})

    def v2_playbook_on_play_start(self, play):
        self._log({"play": play.get_name(),
                   "playbook": self.main_playbook,
                   "id": self.execution_id})

    def v2_runner_on_start(self, host, task):
        self._log({"host": host.get_name(),
                   "task": task.name,
                   "playbook": self.main_playbook,
                   "id": self.execution_id})

    def v2_playbook_on_start(self, playbook):
        if not self.main_playbook:
            self.main_playbook = playbook._file_name.split('/')[-1].split('.')[0]
            self.execution_id = str(uuid.uuid4())
            self._log({"play": "START",
                       "playbook": self.main_playbook,
                       "id": self.execution_id})

    def v2_playbook_on_stats(self, stats):
        failed = False
        unreachable = False
        for host in stats.failures:
            self._log({"play": "FAILED",
                       "host": host,
                       "playbook": self.main_playbook,
                       "id": self.execution_id})
            failed = True
        for host in stats.dark:
            self._log({"play": "UNREACHABLE",
                       "host": host,
                       "playbook": self.main_playbook,
                       "id": self.execution_id})
            unreachable = True
        if not failed and not unreachable:
            self._log({"play": "SUCCESS",
                       "playbook": self.main_playbook,
                       "id": self.execution_id})
