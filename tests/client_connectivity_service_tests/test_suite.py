import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestClientConnectivityService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_search_google(self):
        self.driver.get("https://www.google.com/")
        self.assertIn("Google", self.driver.title)
        elem = self.driver.find_element_by_name("q")
        elem.send_keys("selenium")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in self.driver.page_source


if __name__ == '__main__':
    unittest.main()

