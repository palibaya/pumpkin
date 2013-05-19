from django.test import TestCase
from pumpkin.models import Job

class JobTestCase(TestCase):
    fixtures = ['auth.json','testserver.json', 'project.json',
                'job.json', 'build.json']

    def test_run(self):
        job = Job.objects.get(id=1)
        job.run()
        build_logs = job.build_logs.order_by('sequence')
        statuses = [l.status for l in build_logs]
        self.assertEqual(['success', 'success', 'failure'], statuses)
