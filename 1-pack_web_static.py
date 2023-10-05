#!/usr/bin/python3
"""Fabric script to generate a .tgz archive from web_static folder"""

from fabric.api import local
from datetime import datetime


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
