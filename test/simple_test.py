#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from model.tree_model import TreeDO
import inspect
import sys,pkgutil
import pandas
from base import bean_util
from routes import ctl
import requests
import json


def getattr_static(cls, **kv):
    for k, v in kv.items():
        if hasattr(cls, k):
            print(inspect.getattr_static(cls,k))


class SimpleTest(unittest.TestCase):
    def test_dic_to_obj(self):
        param_map = {
            "tree_level": 1,
            "valid1": True,
            "english_name": "test_name"
        }
        cate = bean_util.to_obj(TreeDO, **param_map)
        print(inspect.isclass(cate))

    def test_crud(self):
        param = {
            "tree_level": 1,
            "valid": True,
            "english_name": "test_name"
        }
        response = requests.post(api_url, data=json.dumps(param))
        print(response.text)


if __name__ == "__main__":
    unittest.main()
