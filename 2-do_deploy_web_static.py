#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""

from fabric.api import env, put, run
from datetime import datetime
from os import path

env.hosts = ['18.209.178.16', '54.173.85.21']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Distribute an archive to the web servers and deploy it.

    Args:
        archive_path (str): The path to the archive to deploy.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not (path.exists(archive_path)):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web servers
        put(archive_path, '/tmp/')

        # Extract archive to /data/web_static/releases/<archive_filename_without_extension>/
        archive_filename = os.path(archive_path)
        folder_name = archive_filename.replace('.tgz', '')

        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_filename, folder_name))

        # Remove the uploaded archive
        run('rm /tmp/{}'.format(archive_filename))

        # Move files to final location
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(folder_name, folder_name))

        # Remove the old symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(folder_name))

        return True

    except Exception as e:
        return False
