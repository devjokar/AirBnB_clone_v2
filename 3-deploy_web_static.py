#!/usr/bin/python3
'''distribute an archive to web servers using the function do_deploy'''

import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


env.hosts = ['100.26.50.2', '']


def do_pack(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    ttime = datetime.now()
    tpath = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        ttime.year, ttime.month, ttime.day, ttime.hour,
        ttime.minute, ttime.second
    )
    try:
        print("Packing web_static to {}".format(tpath))
        local("tar -cvzf {} web_static".format(tpath))
        archize_size = os.stat(tpath).st_size
        print("web_static packed: {} -> {} Bytes".format(tpath, archize_size))
    except Exception:
        tpath = None
    return tpath


def do_deploy(archive_path):
    """Deploys the static files to the host servers.
    Args:
        archive_path (str): The path to the archived static files.
    """
    if not os.path.exists(archive_path):
        return False
    fname = os.path.basename(archive_path)
    dname = fname.replace(".tgz", "")
    rpath = "/data/web_static/releases/{}/".format(dname)
    status = False
    try:
        put(archive_path, "/tmp/{}".format(fname))
        run("sudo mkdir -p {}".format(rpath))
        run("sudo tar -xzf /tmp/{} -C {}".format(fname, rpath))
        run("sudo rm -rf /tmp/{}".format(fname))
        run("sudo mv {}web_static/* {}".format(rpath, rpath))
        run("sudo rm -rf {}web_static".format(rpath))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(rpath))
        print('New version deployed!')
        status = True
    except Exception:
        status = False
    return status


def deploy():
     """Create and distribute an archive to a web server."""
     file = do_pack()
     if file is None:
         return False
     return do_deploy(file)
