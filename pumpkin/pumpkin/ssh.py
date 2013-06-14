import paramiko


class SSHClient(object):

    def __init__(self, server):
        self.server = server
        self.params = {}
        self.list_param = []
        self.list_cmd = []

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko\
                                                .AutoAddPolicy())
        self.client.connect(hostname=self.server.host,
                            port=self.server.port,
                            username=self.server.user_login,
                            password=self.server.user_password)

    def close(self):
        self.list_cmd = []
        self.client.close()

    def set_params(self, params):
        self.params = params
        for k in self.params:
            self.list_param.append('export %s=%s' % (k, self.params[k]))


    def add_param(self, **kwargs):
        self.params.update(kwargs)

    def add_command(self, cmd):
        #cmd = cmd.replace('\r','\n')
        cmds = filter(lambda x: len(x.strip()) > 0, cmd.split('\n'))
        self.list_cmd += cmds

    def execute(self):
        list_cmd = self.list_param + self.list_cmd
        #cmd = ' && '.join(list_cmd)
        cmd = '\n'.join(list_cmd)
        return self.client.exec_command(cmd)

    def exec_commands(self, cmd, params=None):
        """
        all in one commands
        :param cmd:
        :param params:
        """
        if not params:
            params = {}
        self.list_cmd = filter(lambda x: len(x.strip()) > 0,
                               cmd.split('\n'))
        self.set_params(params)
        return self.execute()

