#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""

from fabric.api import env, put, run
from datetime import datetime
import os

env.hosts = ['18.209.178.16', '54.173.85.21']
env.user = 'ubuntu'


def do_pack():
    """
        return the archive path if archive has generated correctly
    """

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_f_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_archive = local("tar -cvzf {} web_static".format(archived_f_path))

    if t_gzip_archive.succeeded:
        return archived_f_path
    else:
        return None


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
        tmp_archive = "/tmp/{}".format(archive_path.split("/")[1])
        releases = "/data/web_static/releases/"
        archive_name = archive_path.split("/")[1].split(".")[0]
        current = "/data/web_static/current"
        full_path = "{}{}/".format(releases, archive_name)

        put(archive_path, tmp_archive)

        run("cd /home/{}".format(env.user))

        run("sudo mkdir -p {}".format(full_path))

        run("sudo tar -xzf {} -C {}".format(tmp_archive,
                                            full_path))

        run("sudo rm -rf {}".format(tmp_archive))

        run("sudo mv {}web_static/* {}".format(full_path, full_path))

        run("sudo rm -rf /data/web_static/current")

        run("sudo ln -sf {} {}".format(full_path, current))

        print("New version deployed!")

        return True
    except Exception as e:
        return False
