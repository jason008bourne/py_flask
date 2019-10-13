#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

""" 生成DB实例 """
db = SQLAlchemy()

flask_app = Flask(__name__, instance_relative_config=True)

