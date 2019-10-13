#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app
from instance import db
from base import bean_util
from base.model import Page
from flask import jsonify


class Result:

    @staticmethod
    def success(obj):
        return jsonify(code=1, body=obj)

    @staticmethod
    def fail(code=500, message="system error", obj=None):
        return jsonify(code=code, message=message, body=obj)

    @staticmethod
    def fail_error(biz_error, obj=None):
        if not biz_error:
            return Result.fail()
        return jsonify(code=biz_error.code, message=biz_error.message, body=obj)


class BizError(Exception):

    ERROR_VALIDATE = 400

    ERROR_BIZ = 450

    ERROR_SYS = 500

    def __init__(self, code, message):
        super().__init__(code, message)
        self.code = code
        self.message = message


class BizUtil:

    NOT_NULL_MSG = "不能为空"

    @staticmethod
    def check_assert(obj, obj_name):
        BizUtil.assert_condition(not obj, obj_name + BizUtil.NOT_NULL_MSG)

    @staticmethod
    def assert_condition(true_or_false: bool, msg: str):
        if true_or_false:
            raise BizError(BizError.ERROR_VALIDATE, msg)

    @staticmethod
    def handle_error(msg: str, err: Exception):
        if not msg:
            msg = "system error"

        if isinstance(err, BizError):
            return Result.fail_error(err)

        app.logger.exception(msg)

        return Result.fail(BizError.ERROR_SYS,msg)


class BaseService:

    @staticmethod
    def insert(po):
        if not po:
            return po
        db.session.add(po)
        return po

    @staticmethod
    def insert_batch(po_list):
        if not po_list:
            return po_list
        db.session.bulk_save_objects(po_list)
        return po_list

    @staticmethod
    def update_by_id(po):
        obj = BaseService.select_by_id(po)
        BizUtil.assert_condition(not obj, "id为" + str(po.id) +"的实体不存在")
        """balabala 写你的逻辑 """
        po_dict = bean_util.sqlalchemy_obj_to_dict(po)
        bean_util.to_obj(obj, **po_dict)
        return obj

    @staticmethod
    def update_by_where(po, where_po):
        if not po:
            return po
        q = BaseService.gen_query(where_po)
        """拼接其他条件"""
        po_dict = bean_util.sqlalchemy_obj_to_dict(po)
        q.update(**po_dict)
        return po

    @staticmethod
    def select_one(po):
        if not po:
            return po
        q = BaseService.gen_query(po)
        """拼接其他条件"""
        return q.first()

    @staticmethod
    def select_by_id(po):
        if not po:
            return po
        query = po.__class__.query
        if not po.id:
            return None
        return query.get(po.id)

    @staticmethod
    def select_by_where(po):
        if not po:
            return None
        page = Page.gen_page(**{})
        if po.page:
            page = po.page
        q = BaseService.gen_query(po)
        page_result = q.paginate(page.page, page.size,False)
        return page_result.items

    @staticmethod
    def delete_by_id(po):
        if not po:
            return po
        obj = BaseService.select_by_id(po)
        BizUtil.assert_condition(not obj, "id为" + str(po.id) +"的实体不存在")
        db.session.delete(obj)
        """拼接其他条件"""
        return obj

    @staticmethod
    def delete_by_where(po):
        if not po:
            return 0
        q = BaseService.gen_query(po)
        row_count = q.delete(synchronize_session=False)
        """拼接其他条件"""
        return row_count

    @staticmethod
    def count_by_where(po):
        if not po:
            return 0
        q = BaseService.gen_query(po)
        return q.count()

    @staticmethod
    def gen_query(po):
        if not po:
            return None
        where_dict = bean_util.sqlalchemy_obj_to_dict(po)
        cls = po.__class__
        q = cls.query
        if where_dict:
            q = q.filter_by(**where_dict)
        if po.ids:
            field = cls.id
            if po.in_field:
                field = getattr(cls, po.in_field)
            q = q.filter(field.in_(po.ids))
        return q

    @staticmethod
    def commit():
        db.session.commit()
