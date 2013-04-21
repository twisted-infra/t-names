"""
Support for DNS service installation and management.
"""

from fabric.api import run, settings

from braid import authbind, git, cron
from braid.twisted import service

# TODO: Move these somewhere else and make them easily extendable
from braid import config


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
            run('ln -nsf {}/start {}/start'.format(self.srcDir, self.binDir))
            self.task_update()
            cron.install(self.serviceUser, '{}/crontab'.format(self.srcDir))

    def task_update(self):
        """
        Update config.
        """
        with settings(user=self.serviceUser):
            # TODO: This is a temp location for testing
            git.branch('https://github.com/twisted-infra/t-names', self.srcDir)
            # TODO restart


globals().update(TwistedNames('t-names').getTasks())
