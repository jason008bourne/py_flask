#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from .test_base import BaseTestCase
import requests
import json
from biz import tree_biz
from biz.tree_biz import TreeService

api_url = "http://127.0.0.1:5000/open"
headers = {"token": "", "Content-Type": "application/json;charset=UTF-8"}


class TestTreeBiz(BaseTestCase):

    def test_get(self):
        param = {
            "tree_level": 1,
            "valid": True,
            "english_name": "test_crud"
        }
        print(tree_biz.get(**param))

    def test_save(self):
        param = {
            "tree_level": 1,
            "valid": True,
            "english_name": "test_crud"
        }
        print(tree_biz.save(**param))

    def test_edit(self):
        param = {
            "id": 14,
            "valid": False,
            "english_name": "test_crud2"
        }
        print(tree_biz.edit(**param))

    def test_list(self):
        param = {
            "tree_level": 1,
            "valid": False,
            "english_name": "test_crud2"
        }
        print(tree_biz.query(**param))

    def test_remove(self):
        param = {
            "id": 1,
            "valid": False,
            "english_name": "test_crud2"
        }
        print(tree_biz.remove(**param))

    def test_remove_by_where(self):
        param = {
            "tree_level": 1,
            "valid": False,
            "english_name": "test_crud2"
        }
        print(TreeService.remove(**param))


class TestTreeCtl(unittest.TestCase):

    def test_get(self):
        param = {
            "tree_level": 1,
            "valid": False,
            "english_name": "test_crud1"
        }
        response = requests.post(api_url + "/tree/get", data=json.dumps(param), headers=headers)
        print(response.text)

    def test_save(self):
        param = {
            "tree_level": 1,
            "valid": False,
            "english_name": "test_crud1"
        }
        response = requests.post(api_url + "/tree/save", data=json.dumps(param), headers=headers)
        print(response.text)

    def test_edit(self):
        param = {
            "id": 15,
            "valid": True,
            "english_name": "test_crud2"
        }
        response = requests.post(api_url + "/tree/edit", data=json.dumps(param), headers=headers)
        print(response.text)

    def test_list(self):
        param = {
            "tree_level": 1,
            "valid": True,
            "english_name": "test_crud2"
        }
        response = requests.post(api_url + "/tree/list", data=json.dumps(param), headers=headers)
        print(response.text)

    def test_remove(self):
        param = {
            "id": 15,
            "valid": False,
            "english_name": "test_crud1"
        }
        response = requests.post(api_url + "/tree/remove", data=json.dumps(param), headers=headers)
        print(response.text)


if __name__ == "__main__":
    unittest.main()
