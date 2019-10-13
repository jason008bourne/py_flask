#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import manager
from instance import db


class BaseTestCase(unittest.TestCase):

    ''' 继承自unittest.TestCase类。 '''
    def setUp(self):
        app = manager.create_app("dev.py")
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()


if __name__ == "__main__":
    unittest.main()
