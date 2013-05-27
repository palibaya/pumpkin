import paramiko

class SSHClient(object):

    def __init__(self, server):
        self.server = server
        self.params = {}
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko\
                                                .AutoAddPolicy())
        self.client.connect(hostname=server.host,
                            port=server.port,
                            username=server.user_login,
                            password=server.user_password)
        self.cmds = []

    def set_params(self, params):
        self.params = params

    def add_param(self, **kwargs):
        self.params.update(kwargs)

    def add_command(self, cmd):
        self.cmds.append(cmd)

    def execute(self):
        cmd = ''
        for k in self.params:
            cmd += 'export %s=%s && '
        for c in self.cmds:
            cmd += '%s &&'
        return self.client.exec_command(cmd)

    def exec_commands(self, cmd, params={}):
        '''
        all in one commands
        '''
        self.cmds = filter(lambda x: len(x.strip()) > 0, cmd.split('\n'))
        self.set_params(params)
        return self.execute()

    def close(self):
        self.client.close()

