#!/usr/bin/env python
# -*- coding: utf-8 -*-

from instance import db
from base import bean_util

copy_property_list = ["has_next", "total"]


class Page:
    __default_size = 500
    default_max_page = 50
    default_max_size = 1000

    KEY_SIZE = "size"
    KEY_PAGE = "page"

    @staticmethod
    def gen_page(**kwargs):
        if not kwargs:
            return Page(None, None)
        size = kwargs.get(Page.KEY_SIZE, None)
        page = kwargs.get(Page.KEY_PAGE, None)
        return Page(size, page)

    def __init__(self, size=__default_size, page=1):
        self.page = page
        self.size = size
        self.page_protect()

    def page_protect(self):
        if not self.page or self.page < 0 or self.page > self.default_max_page:
            self.page = 1
        if not self.size or self.size < 0 or self.size > self.default_max_size:
            self.size = Page.__default_size
            # self.offset = (self.page-1) * self.size

    def copy_page(self, sqlalchemy_page):
        self.items = bean_util.sqlalchemy_list_to_dict_list(sqlalchemy_page.items)
        for k in copy_property_list:
            setattr(self, k, getattr(sqlalchemy_page, k))
        return self

    # def gen_total_page(self):
    #     result = 0
    #     if not self.total and not self.size:
    #         result = self.total // self.size
    #
    #     if self.total % self.size != 0:
    #         ++result
    #     if result == 0:
    #         result = 1
    #
    #     return result


class BaseDO(db.Model):
    __abstract__ = True
    """
    主键ID
    """
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)

    """
    创建时间
    """
    create_time = db.Column(db.DateTime, default=db.func.now())

    """
    更新时间
    """
    update_time = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    page = None

    ids = None

    in_field = None

    """ 根据字典返回一个sqlalchemy 查询对象,拼接好了各种等于过滤"""
    @classmethod
    def gen_query(cls, **kv):
        q = cls.query
        query_dict = cls.to_query_dict(**kv)
        if query_dict:
            q = q.filter_by(**query_dict)
        return q

    # 生成的都是orm中的字段，其他用bean_util
    @classmethod
    def to_query_dict(cls, **kv):
        res_dict = {}
        for key in cls.__mapper__.c.keys():
            v = kv.get(key, None)
            if not v and not isinstance(v, bool):
                continue
            res_dict[key] = v
        return res_dict
