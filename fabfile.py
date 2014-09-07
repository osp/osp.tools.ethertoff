from fabric.api import run, cd, env, local, sudo

env.hosts = ['osp@osp.kitchen']
env.path = '/home/osp/apps/vj14/ethertoff'

def getdb():
    pass

def deploy():
    with cd(env.path):
        run('git pull origin vj14')
        run('/home/osp/apps/venvs/vj14/bin/python manage.py collectstatic --noinput')
        sudo('/usr/bin/supervisorctl restart vj14')

def index():
    with cd(env.path):
        run('/home/osp/apps/venvs/vj14/bin/python manage.py index')
