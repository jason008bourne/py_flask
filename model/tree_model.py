#!/usr/bin/env python
# -*- coding: utf-8 -*-

from instance import db
from base.model import BaseDO


class TreeDO(BaseDO):

    __tablename__ = "test_tree"

    # 类目英文名称
    english_name: str = db.Column(db.String(64), unique=True)

    # 类目中文名称
    chinese_name: str = db.Column(db.String(64), index=True)

    # 父类目id
    parent_id: int = db.Column(db.Integer)

    # 类目层级
    tree_level: int = db.Column(db.Integer)

    # 是否叶子节点
    leaf: bool = db.Column(db.Boolean, default=False)

    # 是否是有效类目
    valid: bool = db.Column(db.Boolean, default=False)


class TreeDTO(TreeDO):
    a: int
    b: str


