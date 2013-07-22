from fabric.api import run, sudo, cd, put, task

@task
def initial_package_setup():
    sudo('apt-get -y update')
    #apt-get = package manager / manages dependencies
    sudo('apt-get -y upgrade')
    #apt-get = package manager / downloads updates and installs them
    sudo('apt-get install nginx supervisor python-pip libevent-dev gcc python-dev python-libxml2 git python-lxml python-mysqldb python-imaging subversion python2.7-sqlite libcurl-dev libcurl4-openssl-dev libsqlite3-dev sqlite3 python2.7-ldap')
    sudo('pip install -U pip')#pip install = update itself
    #apt-get /nginx = webserver - handles static file requests/ acts as proxy server to gunicorn
    #apt-get /supervisor = watches the processes/ runs in the foreground, restarts them on quit
    #apt-get /python-pip = python installer package + manage dependencies
    #apt-get /libevent-dev = library that abstracts away the internals of eventing, and gives applications a generic interface that they can use to kernel event libraries
    #apt-get /standard c/c++ complier
    #apt-get /python-dev = required python development files, required for building extensions
    #apt-get /python-libxml2 = library to parse markup language
    #apt-get /git = distributed version control *used to download packages using pip*
    #apt-get /python-lxml = library to parse markup language *lmxl uses libxml
    #apt-get /python-mysqldb = pythons driver to interface with mysql servers
    #apt-get /python-imaging = *pil* / python imaging library - manipulate images in a pythonic way
    #apt-get /subversion = centralized version control *used to download packages using pip*
    #apt-get /sqlite = flatfile database used to store data in a flat file template
    #apt-get /libcurl-dev = interface to fetch and manipulate urls
    #apt-get /libcurl4-openssl-dev = interface to fetch and manipulate urls
    #apt-get /libsqlite3-dev = used to read and manipulate database (sqlite)files
    #apt-get /sqlite3
    #apt-get /python2.7-ldap = python query library used to query ldap servers

@task
def setting_up_datamyne():
    with cd('/var/www/'):
        sudo('rm -r')#completely remove everything within nginx basic files
        sudo('chown ubuntu:ubuntu -R * ')
        run ('git clone git@github.com:ParsonsAMT/datamining.git')#cloned datamyne

    sudo ('pip install -r pip-known-stable.txt')
    #-r takes a requirements file / pip-known-stable lists all known stable dependencies of the datamyne software
    sudo ('pip install gunicorn gevent')
    #gevent = python library that encapsulates libevent / gunicorn = server WSGI (web server gateway interface)

@task
def setup_nginx():
    sudo('/etc/init.d/nginx stop')
    sudo ('rm /etc/nginx/sites-available/default')
    put('../config_files/nginx/default', '/etc/nginx/sites-available/default', use_sudo=True)
    sudo('/etc/init.d/nginx start')

@task
def setup_supervisor():
    sudo('/etc/init.d/supervisor stop')
    put('../config_files/supervisor_config/gunicorn.conf', '/etc/supervisor/conf.d/gunicorn.conf', use_sudo=True)
    sudo('/etc/init.d/supervisor start')

@task
def setup_and_deploy():
    initial_package_setup()
    setting_up_datamyne()
    setup_nginx()
    setup_supervisor()
