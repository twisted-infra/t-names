"""
Support for DNS service installation and management.
"""

from fabric.api import run, settings

from braid import authbind, git, cron
from braid.twisted import service

from braid import config
_hush_pyflakes = [ config ]


class TwistedNames(service.Service):

    def task_install(self):
        """
        Install t-names, a Twisted Names based DNS server.
        """
        # Bootstrap a new service environment
        self.bootstrap()

        # Setup authbind
        authbind.allow(self.serviceUser, 53)

        with settings(user=self.serviceUser):
            run('ln -nsf {}/start {}/start'.format(self.configDir, self.binDir))
            self.task_update()
            cron.install(self.serviceUser, '{}/crontab'.format(self.configDir))


    def task_update(self):
        """
        Update config and restart.
        """
        with settings(user=self.serviceUser):
            git.branch('https://github.com/twisted-infra/t-names', self.configDir)
        self.task_restart()



globals().update(TwistedNames('t-names').getTasks())
