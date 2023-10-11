import unittest
from aiohttp import web
from webserver import handle, get_stats, get_unique_stats, get_stats_values, generate_unique_id, insert_data_base, \
    get_html_data_handle, get_html_data_unique_stats, check_browsers, get_set_cookie
from unittest import mock
import requests
import sqlite3


class TestCases(unittest.TestCase):
    def setUp(self):
        self.resp = requests.get("http://104.248.81.33:8080/")

    def test_generate_unique_id(self):
        unique_id = generate_unique_id()
        self.assertIsInstance(unique_id, str)
        # Add more assertions for the generated unique ID if needed

    def test_get_html_data_unique_stats(self):
        values = {
            'unique_day': 10,
            'unique_month': 100,
            'unique_year': 1000,
            'unique_total': 5000
        }
        html_data = get_html_data_unique_stats(values)
        self.assertIsNotNone(html_data)

    def test_check_browsers(self):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        browser = check_browsers(user_agent)
        self.assertEqual(browser, 'Google Chrome')
        # Add more assertions for other browser types if needed

    def test_get_set_cookie(self):
        response_data = mock.Mock()

        user_id_cookie = None
        user_id = get_set_cookie(user_id_cookie, response_data)
        self.assertIsNotNone(user_id)

        user_id_cookie = 'abc123'
        user_id = get_set_cookie(user_id_cookie, response_data)
        self.assertEqual(user_id, user_id_cookie)

    def test_requests(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_get_cookies(self):
        self.assertIsNotNone(self.resp.cookies)

    def test_get_html_data(self):
        html_data = get_html_data_handle()
        self.assertEqual(self.resp.text, html_data)


if __name__ == '__main__':
    unittest.main()
