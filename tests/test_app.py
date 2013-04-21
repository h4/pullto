# coding = utf-8
import os
import json
import unittest
from webtest import TestApp
import app as application

current_dir = os.path.dirname(__file__)


class Test(unittest.TestCase):
    def setUp(self):
        payload_file = os.path.join(current_dir, 'travis-payload.json')

        self.valid_token = '35ca10f4f974ef107cde3243dca2bdd56df683c2b8cdfa45b3c4672c759e9f5a'
        self.invalid_token = 'Broken_Token'
        self.payload = json.load(open(payload_file))

    def test_check_auth(self):
        expected_result = application.check_auth(self.valid_token)
        unexpected_result = application.check_auth(self.invalid_token)

        self.assertTrue(expected_result)
        self.assertFalse(unexpected_result)

    def test_verify_status(self):
        self.assertTrue(application.verify_status(self.payload))

    def test_index_page(self):
        app = TestApp(application.app)

        assert app.get('/', expect_errors=True).status_int == 400
        assert app.post('/', expect_errors=True).status_int == 401

        assert app.post('/', expect_errors=True, headers={'Authorization': self.invalid_token}).status_int == 401
        assert app.post('/', expect_errors=True, headers={'Authorization': self.valid_token}, ).status_int == 500
