from datetime import datetime

from django.conf import settings

import pytz

from pumpkin.models import BuildLog
from pumpkin.ssh import SSHClient
from pumpkin.tools import get_obj

current_tz =  pytz.timezone(settings.TIME_ZONE)

class BaseBuilder(object):

    def __init__(self, build, job_log):
        self.build = build
        self.job_log = job_log

    def run(self):
        raise Exception("Unimplentation methods")

    def get_log(self):
        raise Exception("Unimplentation methods")

    def pre_run(self):
        pass

    def build_run(self):
        self.pre_run()
        self.run()
        self.post_run()

    def post_run(self):
        pass


class BashBuilder(BaseBuilder):

    def __init__(self, *args, **kwargs):
        super(BashBuilder, self).__init__(*args, **kwargs)
        self.client = SSHClient(self.build.job.project.server)


    def _create_log(self):
        self.log = BuildLog()
        self.log.build = self.build
        self.log.sequence = self.build.sequence
        self.log.job = self.build.job
        self.log.job_log = self.job_log
        self.log.content = self.build.content
        self.log.begin = current_tz.localize(datetime.now())

    def _save_log(self):
        if len(self.error_list) > 0:
            self.log.status = 'failure'
        else:
            self.log.status = 'success'

        print self.output_list
        self.log.output = ''.join(self.output_list)
        self.log.error = ''.join(self.error_list)

        self.log.end = current_tz.localize(datetime.now())
        self.log.save()

    def get_log(self):
        if not hasattr(self, 'log'):
            raise Exception('Builder has never run')
        return self.log

    def pre_run(self):
        # go to root path of project
        self.pre_command = 'cd $PROJECT_WORKSPACE'
        self.command = self.build.content
        self._create_log()

    def post_run(self):
        self._save_log();


    def run(self):
        #connect ssh
        self.client.set_params(self.build.job.project.get_params())
        self.client.connect()
        #send command
        self.client.add_command(self.pre_command)
        self.client.add_command(self.command)
        stdin, stdout, stderr = self.client.execute()
        #read output
        self.output_list = stdout.readlines()
        self.error_list = stderr.readlines()
        #close ssh session
        self.client.close()

class PythonBuilder(BaseBuilder):

    def run(self):
        pass

class PythonFunctionBuilder(BaseBuilder):

    def run(self):
        ''' implemented method'''
        pass
