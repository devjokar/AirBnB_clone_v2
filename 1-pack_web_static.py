#!/usr/bin/python3
""" Generates a .tgz archive from the contents of the web_static folder """
from os import path
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    """Archives the static files."""
    if not path.isdir("versions"):
        local("mkdir versions")
    d_time = datetime.now()
    tarball = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        d_time.year, d_time.month, d_time.day, d_time.hour, d_time.minute,
        d_time.second
    )
    try:
        local("tar -cvzf {} web_static".format(tarball))
    except Exception:
        tarball = None
    return tarball
