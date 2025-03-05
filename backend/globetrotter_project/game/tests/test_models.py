# game/tests/test_models.py
from django.test import TestCase
from game.models import Destination

class DestinationModelTest(TestCase):
    def test_string_representation(self):
        """Test that the string representation of a Destination is its city name."""
        destination = Destination(city="Paris")
        self.assertEqual(str(destination), "Paris")
