from flask import request
from flask import current_app as app
from routes import open_api as api
from biz import tree_biz
from base.biz import BizUtil
from base.biz import Result


@api.route("/tree/save",  methods=["POST"])
def tree_save():
    try:
        args = request.get_json()
        return Result.success(tree_biz.save(**args))
    except Exception as e:
        return BizUtil.handle_error("save error", e)


@api.route("/tree/edit",  methods=["POST"])
def tree_edit():
    try:
        args = request.get_json()
        return Result.success(tree_biz.edit(**args))
    except Exception as e:
        return BizUtil.handle_error("edit error", e)


@api.route("/tree/get",  methods=["POST"])
def tree_get():
    try:
        args = request.get_json()
        return Result.success(tree_biz.get(**args))
    except Exception as e:
        return BizUtil.handle_error("get error", e)


@api.route("/tree/list",  methods=["POST"])
def tree_list():
    try:
        args = request.get_json()
        return Result.success(tree_biz.query(**args))
    except Exception as e:
        return BizUtil.handle_error("list error", e)


@api.route("/tree/remove",  methods=["POST"])
def tree_remove():
    try:
        args = request.get_json()
        return Result.success(tree_biz.remove(**args))
    except Exception as e:
        return BizUtil.handle_error("remove error", e)

