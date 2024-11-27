import unittest
import os
from app.config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.config = Config()

    def test_get_database_uri(self):
        """Test get_database_uri method."""
     
        basedir = os.path.abspath(os.path.dirname(__file__))[:-5]
        basedir += 'app'
        print(basedir)
        expected_default_uri = 'sqlite:///' + os.path.join(basedir, 'app.db')
        self.assertEqual(self.config.get_database_uri(), expected_default_uri)

    def test_is_sqlalchemy_tracking_enabled(self):
        """Test is_sqlalchemy_tracking_enabled method."""
        self.assertFalse(self.config.is_sqlalchemy_tracking_enabled())

if __name__ == '__main__':
    unittest.main()