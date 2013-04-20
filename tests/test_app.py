# coding = utf-8

import os
import json
import unittest
from webtest import TestApp
import app as application


current_dir = os.path.dirname(__file__)


def test_index_page():
    app = TestApp(application.app)

    assert app.get('/', expect_errors=True).status_int == 400
    assert app.post('/', expect_errors=True).status_int == 401

    token = 'wrong_token'

    assert app.post('/', expect_errors=True, headers={'Authorization': token}).status_int == 401


class Test(unittest.TestCase):
    def test_check_auth(self):

        valid_token = '35ca10f4f974ef107cde3243dca2bdd56df683c2b8cdfa45b3c4672c759e9f5a'
        invalid_token = 'Broken_Token'

        expected_result = application.check_auth(valid_token)
        unexpected_result = application.check_auth(invalid_token)

        self.assertTrue(expected_result)
        self.assertFalse(unexpected_result)

    def setUp(self):
        payload_file = os.path.join(current_dir, 'travis-payload.json')
        self.payload = json.load(open(payload_file))


    def test_verify_status(self):
        self.assertTrue(application.verify_status(self.payload, repository='http: //github.com/svenfuchs/minimal'))
