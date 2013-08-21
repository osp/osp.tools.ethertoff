from fabric.api import run, cd, env, local, sudo


env.hosts = ['osp@osp.constantvzw.org']
env.path = '/home/osp/apps/relearn/relearn.be/'

def getdb():
    pass

def deploy():
    with cd(env.path):
        run('git pull origin master')
        run('/home/osp/apps/venvs/relearn/bin/python manage.py collectstatic --noinput')
        sudo('supervisorctl restart relearn')
