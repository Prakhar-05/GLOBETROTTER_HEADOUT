# game/tests/test_views.py
from django.urls import reverse
from django.test import TestCase
from game.models import Destination

class GlobetrotterViewsTest(TestCase):
    def setUp(self):
        # Create a sample Destination instance for testing views.
        self.destination = Destination.objects.create(
            city="Paris",
            clues=["City of Lights", "Famous for the Eiffel Tower"],
            fun_fact="Paris was once known as Lutetia.",
            trivia=["Home to the Louvre", "Known for fashion"]
        )

    def test_homepage_status_code(self):
        """Test that the homepage returns a 200 status code."""
        url = reverse('index')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

  