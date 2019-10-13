#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import inspect


def to_obj(obj, **kv):
    if inspect.isclass(obj):
        obj = obj()
    if not kv or not obj:
        return obj
    for k, v in kv.items():
        if hasattr(obj, k):
            if not v and not isinstance(v, bool):
                continue
            setattr(obj, k, v)
    return obj


def sqlalchemy_obj_to_dict(obj):
    res_dict = {}
    if not obj:
        return res_dict
    for key in obj.__mapper__.c.keys():
        v_of_k = getattr(obj, key)
        if not v_of_k and not isinstance(v_of_k, bool):
            continue
        res_dict[key] = special_convert(v_of_k)
    return res_dict


def sqlalchemy_list_to_dict_list(list):
    res = []
    if not list:
        return res
    for obj in list:
        obj_dict = sqlalchemy_obj_to_dict(obj)
        if not obj_dict:
            continue
        res.append(obj_dict)
    return res


def special_convert(obj):
    if not obj:
        return obj
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    else:
        return obj
