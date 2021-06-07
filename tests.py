from django.test import TestCase

# Create your tests here.
class URLTests(TestCase):
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_error_detection_page(self):
        response = self.client.get('error_detection/')
        self.assertEqual(response.status_code, 200)
    
    def test_orientation_page(self):
        response = self.client.get('orientation/')
        self.assertEqual(response.status_code, 200)

    def test_word_rules_page(self):
        response = self.client.get('word_rules/')
        self.assertEqual(response.status_code, 200)

    def test_deductive_reasoning_page(self):
        response = self.client.get('deductive_reasoning/')
        self.assertEqual(response.status_code, 200)

    def test_number_fluency_page(self):
        response = self.client.get('number_fluency/')
        self.assertEqual(response.status_code, 200)


