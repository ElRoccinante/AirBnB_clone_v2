#!/usr/bin/python3
"""Script to create a .tgz archive
from web_static folder using do_pack."""

from fabric.api import local, task
from datetime import datetime
import os


@task
def do_pack():
    """Archives the web_static folder."""
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    mkdir = "mkdir -p versions"
    path = "versions/web_static_{}.tgz".format(date)
    print("Packing web_static to {}".format(path))
    if local('{} && tar -cvzf {} web_static'.format(mkdir, path)).succeeded:
        size = os.path.getsize(path)
        print("web_static packed: {} -> {}Bytes".format(path, size))
        return path
    return None
