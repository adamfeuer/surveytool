from fabric.api import *

"""
Base configuration
"""
env.project_name = 'surveytool'
env.database_password = '$(db_password)'
env.python = 'python2.7'
env.hosts = []
env.user = "$(user)"

"""
Environments
"""
def production():
    """
    Work on production environment
    """
    env.settings = 'production' 
    env.hostname = 'research.liveingreatness.com'
    env.env_path = '/opt/webapps/%(hostname)s' % env
    env.log_path = '/opt/webapps/%(hostname)s/logs' % env
    env.repo_path = '%(env_path)s/%(project_name)s' % env
    env.apache_config_path = '/etc/apache2/sites-available/%(hostname)s' % env
    env.hosts = ['research.liveingreatness.com']

def staging():
    """
    Work on staging environment
    """
    env.settings = 'staging'
    env.hostname = 'research-staging.liveingreatness.com' 
    env.env_path = '/opt/webapps/%(hostname)s' % env
    env.log_path = '/opt/webapps/%(hostname)s/logs' % env
    env.repo_path = '%(env_path)s/%(project_name)s' % env
    env.apache_config_path = '/etc/apache2/sites-available/%(hostname)s' % env
    env.hosts = ['research-staging.liveingreatness.com'] 
    
"""
Branches
"""
def stable():
    """
    Work on stable branch.
    """
    env.branch = 'stable'

def master():
    """
    Work on development branch.
    """
    env.branch = 'master'

def branch(branch_name):
    """
    Work on any specified branch.
    """
    env.branch = branch_name
    
"""
Commands - setup
"""
def setup():
    """
    Setup a fresh virtualenv, install everything we need, and fire up the database.
    
    Does NOT perform the functions of deploy().
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])
    
    setup_directories()
    setup_virtualenv()
    clone_repo()
    checkout_latest()
    destroy_database()
    create_database()
    load_data()
    install_requirements()
    install_apache_conf()

def setup_directories():
    """
    Create directories necessary for deployment.
    """
    sshagent_run('mkdir -p %(path)s' % env)
    sshagent_run('mkdir -p %(env_path)s' % env)
    run ('mkdir -p %(log_path)s;' % env)
    sudo('chgrp -R www-data %(log_path)s; chmod -R g+w %(log_path)s;' % env)
    sshagent_run('ln -s %(log_path)s %(path)s/logs' % env)
    
def setup_virtualenv():
    """
<    Setup a fresh virtualenv.
    """
    sshagent_run('virtualenv -p %(python)s --no-site-packages %(env_path)s;' % env)
    sshagent_run('source %(env_path)s/bin/activate; easy_install -U setuptools; easy_install pip;' % env)

def clone_repo():
    """
    Do initial clone of the git repository.
    """
    sshagent_run('git clone git@github.com:adamfeuer/%(project_name)s.git %(repo_path)s' % env)

def checkout_latest():
    """
    Pull the latest code on the specified branch.
    """
    sshagent_run('cd %(repo_path)s; git checkout %(branch)s; git pull origin %(branch)s' % env)

def install_requirements():
    """
    Install the required packages using pip.
    """
    sshagent_run('source %(env_path)s/bin/activate; pip install -E %(env_path)s -r %(repo_path)s/requirements.txt' % env)

def install_apache_conf():
    """
    Install the apache site config file.
    """
    sudo('cp %(repo_path)s/%(project_name)s/configs/%(settings)s/%(project_name)s %(apache_config_path)s' % env)

"""
Commands - deployment
"""
def deploy():
    """
    Deploy the latest version of the site to the server and restart Apache2.
    
    Does not perform the functions of load_new_data().
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])
    
    with settings(warn_only=True):
        maintenance_up()
        
    checkout_latest()
    maintenance_down()
    
def maintenance_up():
    """
    Install the Apache maintenance configuration.
    """
    #sudo('cp %(repo_path)s/%(project_name)s/configs/%(settings)s/%(project_name)s_maintenance %(apache_config_path)s' % env)
    reboot()

def reboot(): 
    """
    Restart the Apache2 server.
    """
    env.host_string = 'root@'+env.hostname
    run('service apache2 restart')
    
def maintenance_down():
    """
    Reinstall the normal site configuration.
    """
    #install_apache_conf()
    reboot()
    
"""
Commands - rollback
"""
def rollback(commit_id):
    """
    Rolls back to specified git commit hash or tag.
    
    There is NO guarantee we have committed a valid dataset for an arbitrary
    commit hash.
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])
    
    maintenance_up()
    checkout_latest()
    git_reset(commit_id)
    maintenance_down()
    
def git_reset(commit_id):
    """
    Reset the git repository to an arbitrary commit hash or tag.
    """
    env.commit_id = commit_id
    sshagent_run("cd %(repo_path)s; git reset --hard %(commit_id)s" % env)

"""
Commands - data
"""
def load_new_data():
    """
    Erase the current database and load new data from the SQL dump file.
    """
    require('settings', provided_by=[production, staging])
    
    maintenance_up()
    destroy_database()
    create_database()
    load_data()
    maintenance_down()
    
def create_database():
    """
    Creates the user and database for this project.
    """
    sshagent_run('echo "CREATE USER %(project_name)s WITH PASSWORD \'%(database_password)s\';" | psql postgres' % env)
    sshagent_run('createdb -O %(project_name)s %(project_name)s -T template_postgis' % env)
    
def destroy_database():
    """
    Destroys the user and database for this project.
    
    Will not cause the fab to fail if they do not exist.
    """
    with settings(warn_only=True):
        sshagent_run('dropdb %(project_name)s' % env)
        sshagent_run('dropuser %(project_name)s' % env)
        
def load_data():
    """
    Loads data from the repository into PostgreSQL.
    """
    sshagent_run('psql -q %(project_name)s < %(path)s/repository/data/psql/dump.sql' % env)
    sshagent_run('psql -q %(project_name)s < %(path)s/repository/data/psql/finish_init.sql' % env)
    
"""
Commands - miscellaneous
"""

def reset_permissions():
    env.host_string = 'root@'+env.hostname
    run("chown -R www-data:www-data %(env_path)s" % env)
    run("chown -R www-data:www-data /var/log/apache2")

def test_local(): 
    """
    Test echo on localhost. Reports the git user settings and the environment $SHELL variable.
    """
    git_username = local('git config --global --get user.name', capture=True)
    local("echo 'Git User: "+git_username+"'")
    local('echo "Current Shell: $SHELL"')


def test_remote(user='root'): 
    """
    Test a remote host, takes user account login name as a single argument
    """
    env.host_string = user+'@'+env.hostname

    git_username    = run('git config --global --get user.name')
    run("echo 'Git User: "+git_username+"'")
    run('echo "Current Shell: $SHELL"')

def echo_host():
    """
    Echo the current host to the command line.
    """
    sshagent_run('echo %(settings)s; echo %(hosts)s' % env)

"""
Deaths, destroyers of worlds
"""
def shiva_the_destroyer():
    """
    Remove all directories, databases, etc. associated with the application.
    """
    with settings(warn_only=True):
        sshagent_run('rm -Rf %(path)s' % env)
        sshagent_run('rm -Rf %(log_path)s' % env)
        sshagent_run('dropdb %(project_name)s' % env)
        sshagent_run('dropuser %(project_name)s' % env)
        sudo('rm %(apache_config_path)s' % env)
        reboot()
        sshagent_run('s3cmd del --recursive s3://%(s3_bucket)s/%(project_name)s' % env)

def host_type():
    sshagent_run('uname -s')

"""
Utility functions (not to be called directly)
"""
def _execute_psql(query):
    """
    Executes a PostgreSQL command using the command line interface.
    """
    env.query = query
    sshagent_run(('cd %(path)s/repository; psql -q %(project_name)s -c "%(query)s"') % env)

def sshagent_run(cmd):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.
    
    Note:: Fabric (and paramiko) can't forward your SSH agent. 
    This helper uses your system's ssh to do so.
    """

    for h in env.hosts:
        try:
            # catch the port number to pass to ssh
            host, port = h.split(':')
            local('ssh -p %s -A %s "%s"' % (port, host, cmd))
        except ValueError:
            local('ssh -A %s "%s"' % (h, cmd))

