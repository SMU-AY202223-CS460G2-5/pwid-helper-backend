from typing import Callable
from unittest import TestCase

from src.app import app as flask_app


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()
        cls.app = flask_app

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCase, cls).tearDownClass()

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.app.testing = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
        super(BaseTestCase, self).tearDown()

    def assertRaisesMessage(self, err: BaseException, func: Callable, *args):
        with self.assertRaises(err.__class__) as error:
            func(*args)
        self.assertEqual(str(error.exception), str(err))
