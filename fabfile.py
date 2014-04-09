from fabric.api import run, cd, env, local, sudo

env.hosts = ['bat@93.191.132.95']
env.path = '/home/bat/apps/relearn.be'

def getdb():
    pass

def deploy():
    with cd(env.path):
        run('git pull origin etherbat')
        run('/home/bat/venvs/relearn/bin/python manage.py collectstatic --noinput')
        sudo('/home/bat/venvs/relearn/bin/supervisorctl restart relearn')

