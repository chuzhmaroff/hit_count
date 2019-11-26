import unittest

import flask_app as app


class TestMethodApp(unittest.TestCase):
    def test_count_user_for_cookie(self):
        with open("count_unique_user_for_cookie.txt", "r") as f:
            count_do = int(f.read())
        app.count_unique_user_for_cookie()
        with open("count_unique_user_for_cookie.txt", "r") as f:
            count_od = int(f.read())
        self.assertNotEqual(count_do, count_od)

    def test_count_user_for_ip(self):
        with open("count_unique_user_for_ip.txt", "r") as f:
            count_do = int(f.read())
        app.count_unique_user_for_ip()
        with open("count_unique_user_for_ip.txt", "r") as f:
            count_od = int(f.read())
        self.assertNotEqual(count_do, count_od)

    """def test_get_ip_address(self):
        a = app.get_ip_address()
        self.assertIsNotNone(a)"""

    def test_get_unique_cookies(self):
        user_agent = "Google Chrome"
        res = app.create_unique_cookie_for_user(user_agent)
        self.assertIsNotNone(res)
        self.assertTrue(type(res) == str)

    def test_get_count_non_unique_user(self):
        count = app.get_count_non_unique_user()
        self.assertTrue(type(count) == str)
        self.assertIsNotNone(count)

    def test_get_info_on_ip(self):
        ip_address = "212.193.78.236"
        result = app.get_info_on_ip(ip_address)
        self.assertIsNotNone(result)

    def test_adding_last_conn_to_txt(self):
        with open('info_last_conn_07112019.txt', 'r') as f:
            text_before = f.read()

        cookies = app.create_unique_cookie_for_user("Google")
        ip_address = "212.193.78.236"

        app.add_user_at_databases(ip_address, cookies)
        app.adding_last_conn_to_txt()
        with open('info_last_conn_07112019.txt', 'r') as f:
            text_after = f.read()
        self.assertNotEqual(text_after, text_before)

    def test_get_coordinates_ip(self):
        ip_address = "212.193.78.236"
        lat = app.get_coordinates_ip(ip_address)[0]
        lon = app.get_coordinates_ip(ip_address)[1]
        self.assertNotEqual(lat, lon)
        self.assertTrue(type(lat) == float)
        self.assertTrue(type(lon) == float)

    def test_do_read(self):
        path = "text_file_for_test.txt"
        res = app.do_read(path)
        self.assertEqual(type(res), str)

    def test_get_bool_unique_ip(self):
        ip_address = "212.193.78.234"  # ip address urfu Turgeneva 4
        result = app.get_bool_unique_ip(ip_address)
        self.assertEqual(result, False)

    def test_create_unique_cookie_for_user(self):
        user_agent = "Google Chrome_v1"
        user_agent2 = "Google Chrome_v2"
        user_agent3 = "Yandex Browser"
        hash1 = app.create_unique_cookie_for_user(user_agent)
        hash2 = app.create_unique_cookie_for_user(user_agent2)
        hash3 = app.create_unique_cookie_for_user(user_agent3)
        self.assertIsNotNone(hash1)
        self.assertIsNotNone(hash2)
        self.assertIsNotNone(hash3)
        self.assertNotEqual(hash1, hash2)
        self.assertNotEqual(hash2,hash3)
        self.assertNotEqual(hash1,hash2,hash3)