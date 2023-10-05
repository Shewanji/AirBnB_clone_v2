#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""

from fabric.api import env, put, run
from datetime import datetime
import os

env.hosts = ['18.209.178.16', '54.173.85.21']
env.user = 'ubuntu'

def do_deploy(archive_path):
    """Distributes an archive to web servers.

    Args:
        archive_path (str): Path to the archive to be deployed.

    Returns:
        bool: True if all operations are successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract archive filename without extension
        archive_filename = os.path.basename(archive_path).split('.')[0]

        # Upload the archive to the /tmp/ directory of the web server
        remote_tmp_path = "/tmp/{}".format(os.path.basename(archive_path))
        c.put(archive_path, remote_tmp_path)

        # Create release directory
        remote_release_dir = "/data/web_static/releases/{}".format(archive_filename)
        c.run("mkdir -p {}".format(remote_release_dir))

        # Uncompress the archive to the release directory
        c.run("tar -xzf {} -C {}".format(remote_tmp_path, remote_release_dir))

        # Delete the archive from the web server
        c.run("rm -f {}".format(remote_tmp_path))

        # Remove old symbolic link
        c.run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new version
        c.run("ln -s {} /data/web_static/current".format(remote_release_dir))

        return True

    except Exception:
        return False
