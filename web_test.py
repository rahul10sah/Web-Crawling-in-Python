import unittest
import hashlib
import requests
from web_crawling import WebCrawler, USER_CREDENTIALS

class WebCrawlerTests(unittest.TestCase):
    def setUp(self):
        self.url = "https://example.com"
        self.depth = 2
        self.crawler = WebCrawler(self.url, self.depth)
    
    def test_crawler_initialization(self):
        """Test if the crawler initializes correctly."""
        self.assertEqual(self.crawler.url, self.url)
        self.assertEqual(self.crawler.max_depth, self.depth)
    
    def test_invalid_url(self):
        """Test if the crawler handles an invalid URL gracefully."""
        invalid_crawler = WebCrawler("invalid_url", 2)
        invalid_crawler.start_crawling()
        self.assertEqual(len(invalid_crawler.links), 0)  

    def test_js_file_extraction(self):
        """Test if JS files are correctly extracted."""
        self.crawler.start_crawling()
        self.assertIsInstance(self.crawler.jsfiles, set)
    
    def test_authentication(self):
        """Test if authentication works correctly."""
        test_password = "password123"
        hashed_password = hashlib.sha256(test_password.encode()).hexdigest()
        self.assertEqual(USER_CREDENTIALS.get("admin"), hashed_password)

if __name__ == "__main__":
    unittest.main()
