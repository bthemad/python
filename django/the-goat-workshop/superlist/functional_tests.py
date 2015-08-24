import unittest
from selenium import webdriver


class HomePageTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_home_page_have_correct_title(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)

    def test_home_page_have_correct_header(self):
        self.browser.get('http://localhost:8000')
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('To-Do', header.text)

    def test_can_introduce_new_items(self):
        self.browser.get('http://localhost:8000')
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertIqual(input_box.get_attripute('placeholder'),
                         'Enter a to-do item')

        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys("\n")

if __name__ == '__main__':
    unittest.main()
