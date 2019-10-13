#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from logging.handlers import TimedRotatingFileHandler
import logging

import instance
import routes
import os


def create_app(env_config):

    flask_app = instance.flask_app
    """
    从instance加载
    """
    # app.config.from_pyfile("hidden_config.py")
    flask_app.config.from_pyfile("default.py")
    flask_app.config["INPUT_DIR"] = os.path.abspath("input")

    """ 从环境变量加载 """
    # app.config.from_envvar("APP_ENV")
    flask_app.config.from_pyfile(env_config)

    instance.db.init_app(flask_app)

    if "local.py" != env_config:
        # 移除默认的控制台输出
        flask_app.logger.removeHandler(flask_app.logger.handlers[0])
        log = logging.getLogger("werkzeug")
        log.setLevel("ERROR")
        # 添加文件日志输出
        file_log_handler = TimedRotatingFileHandler(filename="logs/app.log", when="D",
                                                    interval=1, backupCount=30, encoding="UTF-8", delay=False, utc=True)
        file_log_handler.suffix = "%Y%m%d"
        formatter = logging.Formatter("%(asctime)s %(module)s - %(lineno)d %(levelname)s  %(message)s")
        file_log_handler.setFormatter(formatter)
        flask_app.logger.setLevel(flask_app.config["LOG_LEVEL"])
        flask_app.logger.addHandler(file_log_handler)
    else:
        flask_app.logger.setLevel(flask_app.config["LOG_LEVEL"])

    return flask_app


if __name__ == "__main__":
    env_profile = None
    try:
        env_profile = sys.argv[1]
    except Exception:
        env_profile = "dev"
    app = create_app(env_profile + ".py")
    routes.register_blueprint(app)
    app.run(
        host="0.0.0.0"
    )
