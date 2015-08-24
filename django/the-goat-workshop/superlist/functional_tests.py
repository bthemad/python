import unittest
from selenium import webdriver


class HomePageTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    #  def test_home_page_have_correct_title(self):
        #  self.browser.get('http://localhost:8000')
        #  self.assertIn('To-Do', self.browser.title)

    #  def test_home_page_have_correct_header(self):
        #  self.browser.get('http://localhost:8000')
        #  header = self.browser.find_element_by_tag_name('h1')
        #  self.assertIn('To-Do', header.text)

    def test_can_introduce_new_items_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'),
                         'Enter a to-do item: ')

        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys("\n")

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers',
                      [row.text for row in rows])

if __name__ == '__main__':
    unittest.main()
