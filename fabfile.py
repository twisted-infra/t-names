"""
Support for DNS service installation and management.
"""

from fabric.api import run, settings

from braid import authbind, requiresRoot, git  #, cron
from braid.twisted import service
from braid.config import test, prod, environment


class TwistedNames(service.Service):
    @service.task
    @requiresRoot
    def install(self):
        """
        Install t-names, a Twisted Names based DNS server.
        """
        # Bootstrap a new service environment
        self.bootstrap()

        # Setup authbind
        authbind.install()
        authbind.allow(self.serviceUser, 53)

        # Setup GIT
        git.install()

        with settings(user=self.serviceUser):
            run('ln -nsf {}/start {}/start'.format(self.srcDir, self.binDir))
            self.update()
            # FIXME: Uncomment once cron.py is commited to braid
            #cron.install(env.user, 'Names/crontab')

    @service.task
    def update(self):
        with settings(user=self.serviceUser):
            # TODO: This is a temp location for testing
            git.branch('https://github.com/twisted-infra/t-names', self.srcDir)
            # TODO restart


globals().update(TwistedNames('t-names').getTasks())
