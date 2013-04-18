
from fabric.api import task, settings, run

from braid import authbind, requires_root, git, cron
from braid.twisted import service

serviceName = 't-names'

@task
@requires_root
def install():
    # TODO:
    # - Setup zone files (incl. PYTHONPATH in script if needed)
    # - Rename dns to t-names or whatever (locations, scripts,...)

    # Bootstrap a new service environment
    service.bootstrap(serviceName)

    # Setup authbind
    authbind.install()
    authbind.allow(serviceName, 53)

    git.install()

    with settings(user=serviceName):
        run('ln -nsf Names/start start')
        update()
        cron.install(serviceName, 'Names/crontab')

@task
def update():
    with settings(user=serviceName):
        # TODO: This is a temp location for testing
        git.branch('https://github.com/twisted-infra/t-names', 'Names')
        # TODO restart

globals().update(service.serviceTasks('t-names'))
