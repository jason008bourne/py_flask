#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
import os, pkgutil, importlib
from routes import rest
from routes import ctl

template_dir = os.path.abspath("templates")
print(template_dir)
open_api = Blueprint("open_api", __name__, url_prefix="/open", template_folder=template_dir)


def register_blueprint(app):

    """注册所有ctl下的控制器"""
    ctl_path = "routes.ctl"
    for loader, module_name, is_pkg in pkgutil.walk_packages(ctl.__path__):
        if is_pkg:
            continue
        importlib.import_module("{}.{}".format(ctl_path, module_name))
        # __import__("{}.{}".format(ctl_path, module_name))
    app.register_blueprint(open_api)

