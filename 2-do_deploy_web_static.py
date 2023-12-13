#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers.
"""

from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/my_ssh_private_key'


def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder.
    """
    try:
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -czvf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Distribute an archive to your web servers using Fabric.
    """
    if not exists(archive_path):
        return False

    try:
        filename = archive_path.split("/")[-1]
        no_ext = filename.split(".")[0]

        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, "/tmp/{}".format(filename))

        # Create directory to uncompress the archive
        run("mkdir -p /data/web_static/releases/{}/".format(no_ext))

        # Uncompress the archive
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(filename, no_ext))

        # Remove the archive
        run("rm /tmp/{}".format(filename))

        # Move contents to proper location
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/"
            .format(no_ext, no_ext))

        # Remove the web_static directory
        run("rm -rf /data/web_static/releases/{}/web_static".format(no_ext))

        # Remove the symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(no_ext))

        print("New version deployed!")
        return True

    except Exception as e:
        return False
