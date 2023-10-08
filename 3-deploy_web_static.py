#!/usr/bin/python3
"""Fabric script to generate a .tgz archive from web_static folder"""

from fabric.api import local, env, put, run
from datetime import datetime
from os.path import exists

env.hosts = ['18.209.178.16', '54.173.85.21']
env.user = 'ubuntu'


def do_pack():
    """Generates a .tgz archive from web_static folder.

    Returns:
        str: The archive path if the archive is successfully created,
        None otherwise.
    """
    try:
        # Create a timestamp for the archive filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(timestamp))

        return "versions/web_static_{}.tgz".format(timestamp)

    except Exception as e:
        return None


def do_deploy(archive_path):
    """Distribute an archive to the web servers and deploy it.

    Args:
    archive_path (str): The path to the archive to deploy.

    Returns:
    bool: True if deployment is successful, False otherwise.
    """
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except Exceptios as e:
        return False


def deploy():
    """Script (based on the file 2-do_deploy_web_static.py)
        that creates and distributes an archive
        to your web servers, using the function deploy.
        Return: False if it fails else return value of do_deploy
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
