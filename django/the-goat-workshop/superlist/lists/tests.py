from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page


class HomePageViewTest(TestCase):
    def test_home_page_resturns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertIn('<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.startswith('<html>'))
        self.assertTrue(response.content.endswith('</html>'))
