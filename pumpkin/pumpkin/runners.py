class Runner(object):

    def __init__(self, job):
        self.job = job
        self.project = self.job.project
        self.test_server = self.project.test_server

    def pre_run_job(self):
        pass

    def post_run_job(self):
        pass

    def process_output_build(self, output):
        pass

    def get_status_build(self, output_list, error_list):
        if len(error_list) > 0:
            return 'failure'
        return 'success'
