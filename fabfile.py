from fabric.api import *
import fabric.contrib.project as project
import os

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'root@localhost:22'
dest_path = '/var/www'

# Rackspace Cloud Files configuration settings
env.cloudfiles_username = 'my_rackspace_username'
env.cloudfiles_api_key = 'my_rackspace_api_key'
env.cloudfiles_container = 'my_cloudfiles_container'


def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))

def build():
    local('pelican -s pelicanconf.py')

def rebuild():
    clean()
    build()

def regenerate():
    local('pelican -r -s pelicanconf.py')

def serve():
    local('cd {deploy_path} && python -m SimpleHTTPServer'.format(**env))

def reserve():
    build()
    serve()

def preview():
    local('pelican -s publishconf.py')

def cf_upload():
    rebuild()
    local('cd {deploy_path} && '
          'swift -v -A https://auth.api.rackspacecloud.com/v1.0 '
          '-U {cloudfiles_username} '
          '-K {cloudfiles_api_key} '
          'upload -c {cloudfiles_container} .'.format(**env))

def git_change_branch(branch):
    """Changes from one branch to other in a git repo"""
    local("git checkout {0}".format(branch))

@hosts(production)
def publish():
    local('pelican content -s publishconf.py -o output/')
    master_branch = "master"
    publish_branch = "gh-pages"
    remote = "origin"

    # Push original changes to master
    #push(remote, master_branch)

    # Change to gh-pages branch
    git_change_branch(publish_branch)

    # Merge master into gh-pages
    git_merge_branch(master_branch)

    # Generate the html
    generate(ABS_ROOT_DIR)

    # Commit changes
    now = time.strftime("%d %b %Y %H:%M:%S", time.localtime())
    git_commit_all("Publication {0}".format(now))

    # Push to gh-pages branch
    git_push(remote, publish_branch)

    # go to master
    git_change_branch(master_branch)
