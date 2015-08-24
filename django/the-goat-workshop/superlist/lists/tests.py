from django.test import TestCase
from django.http import HttpRequest

from django.template.loader import render_to_string

from lists.views import home_page


class HomePageViewTest(TestCase):
    def test_home_page_resturns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_template = render_to_string('home.html')

        self.assertEqual(expected_template, response.content)
