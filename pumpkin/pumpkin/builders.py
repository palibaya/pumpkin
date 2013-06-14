from datetime import datetime

from django.conf import settings

import pytz

from pumpkin.models import BuildLog
from pumpkin.ssh import SSHClient

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
        build_log = BuildLog()
        build_log.build = self.build
        build_log.sequence = self.build.sequence
        build_log.job = self.build.job
        build_log.job_log = self.job_log
        build_log.command = self.build.command
        build_log.begin = current_tz.localize(datetime.now())
        return build_log

    def _save_log(self, build_log, output_list, error_list):
        if len(error_list) > 0:
            build_log.status = 'failure'
        else:
            build_log.status = 'success'
        build_log.output = ''.join(output_list)
        build_log.error = ''.join(error_list)

        build_log.end = current_tz.localize(datetime.now())
        build_log.save()

    def get_log(self):
        if not hasattr(self, 'build_log'):
            raise Exception('Builder has never run')
        return self.build_log

    def run(self):
        build_log = self._create_log()
        #initial ssh
        self.client.set_params(self.build.job.project.get_params())
        self.client.connect()
        #command
        self.client.add_command(self.build.command)
        stdin, stdout, stderr = self.client.execute()
        #read outupt
        output_list, error_list = stdout.readlines(), stderr.readlines()
        #close ssh session
        self.client.close()
        #save log
        self._save_log(build_log, output_list, error_list)
        self.build_log = build_log


class PythonFunctionBuilder(object):

    def get_log(self):
        raise Exception("Unimplentation methods")

    def run(self):
        ''' implemented method'''
        pass
