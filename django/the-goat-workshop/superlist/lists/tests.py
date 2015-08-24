from django.test import TestCase
from django.http import HttpRequest

from django.template.loader import render_to_string

from lists.views import home_page


class HomePageViewTest(TestCase):
    def test_home_page_users_correct_template(self):
        request = HttpRequest()
        response = home_page(request)
        expected_template = render_to_string('home.html')

        self.assertEqual(expected_template, response.content)

    def test_home_page_can_store_post_requests(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'new item'
        response = home_page(request)

        expected_content = render_to_string(
            'home.html',
            {'new_item_text': 'new item'})

        self.assertEqual(response.content, expected_content)
