import json
import os
import tempfile
import unittest

from flask import render_template

import app


class FlaskBlockyTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        self.headers = [
            ('Content-Type', 'application/json'),
            ('X-Requested-With', 'XMLHttpRequest'),
        ]

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_renders_content_block(self):
        with self.app as c:
            response = c.get('/', headers=self.headers)
            assert response.status_code == 200

            json_response = json.loads(response.data)
            assert 'blocks' in json_response
            assert filter(
                lambda x: x['name'] == 'content', json_response['blocks']
            )

    def test_render_template(self):
        with self.app as c:
            response = c.get('/')
            assert response.status_code == 200

            expected = render_template('response.html')

            assert expected == response.data

if __name__ == '__main__':
    unittest.main()