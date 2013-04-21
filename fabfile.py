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
        # Bootstrap a new service environment
        self.bootstrap()

        # Setup authbind
        authbind.install()
        authbind.allow(self.serviceUser, 53)

        # Setup GIT
        git.install()

        with settings(user=self.serviceUser):
            run('ln -nsf Names/start start')
            self.update()
            # FIXME: Uncomment once cron.py is commited to braid
            #cron.install(env.user, 'Names/crontab')

    @service.task
    def update(self):
        with settings(user=self.serviceUser):
            # TODO: This is a temp location for testing
            git.branch('https://github.com/twisted-infra/t-names', 'Names')
            # TODO restart


globals().update(TwistedNames('t-names').getTasks())
