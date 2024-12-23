import unittest
from config_parser import parse_config


class TestConfigParser(unittest.TestCase):

    def test_parse_config_with_constants(self):
        config_text = """
        admin_password -> 12345;
        user_password -> ^admin_password;
        users = [admin: ^admin_password, guest: ^user_password];
        """
        parsed = parse_config(config_text)
        self.assertEqual(parsed['admin_password'], '12345')
        self.assertEqual(parsed['user_password'], '12345')
        self.assertEqual(parsed['users'], {'admin': '12345', 'guest': '12345'})

    def test_parse_db_config(self):
        config_text = """
        db_host -> localhost;
        db_port -> 5432;
        db_name -> my_database;
        connection_string -> ^db_host:^db_port/@^db_name;
        """
        parsed = parse_config(config_text)
        self.assertEqual(parsed['connection_string'], 'localhost:5432/@my_database')

    def test_parse_env_config(self):
        config_text = """
        dev_url -> http://localhost:3000;
        prod_url -> https://example.com;
        environment -> dev;
        current_url -> ^dev_url;
        """
        parsed = parse_config(config_text)
        self.assertEqual(parsed['current_url'], 'http://localhost:3000')

    def test_invalid_constant_reference(self):
        config_text = """
        user_password -> ^undefined_password;
        """
        with self.assertRaises(SyntaxError):
            parse_config(config_text)


if __name__ == "__main__":
    unittest.main()
