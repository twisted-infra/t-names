
from fabric.api import put, task, cd, settings, run

from braid import authbind, requires_root, git
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

@task
def update():
    with settings(user=serviceName):
        # TODO: This is a temp location for testing
        git.branch('https://github.com/twisted-infra/t-names', 'Names')
        # TODO restart


@task
def start():
    with settings(user=serviceName):
        run('./start', pty=False)


@task
def stop():
    with settings(user=serviceName):
        run('./stop')


@task
def restart():
    stop()
    start()

@task
def log():
    with settings(user=serviceName):
        run('tail -f twistd.log')
