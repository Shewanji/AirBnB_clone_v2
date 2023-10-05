#!/usr/bin/python3
"""Fabric script to generate a .tgz archive from web_static folder"""

from fabric.api import local, task
from datetime import datetime


@task
def do_pack():
    """Generates a .tgz archive from web_static folder.

    Returns:
        str: The archive path if the archive is successfully created,
        None otherwise.
    """
    try:
        # Create a timestamp for the archive filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Define the archive filename
        archive_filename = f"web_static_{timestamp}.tgz"

        # Create the 'versions' directory if it doesn't exist
        c.run("mkdir -p versions")

        # Compress the contents of the 'web_static' directory into the archive
        c.local(f"tar -czvf versions/{archive_filename} web_static")

        # Return the archive path if it was created successfully
        return f"versions/{archive_filename}"
    except Exception as e:
        return None
