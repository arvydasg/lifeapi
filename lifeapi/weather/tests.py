from django.test import TestCase
from .models import Weather

# Unit Test for Model Creation
class WeatherModelTest(TestCase):
    def test_weather_creation(self):
        weather = Weather.objects.create(date="2023-06-21", temperature=25.5)
        self.assertEqual(weather.date, "2023-06-21")
        self.assertAlmostEqual(weather.temperature, 25.5, places=2)
        print(f"{weather.date} and {weather.temperature} are saved to the fake database and soon will be destroyed")

# # Validation Test for Required Fields
# class WeatherValidationTest(TestCase):
#     def test_date_field_required(self):
#         with self.assertRaises(ValueError):
#             Weather.objects.create(date="", temperature=25.5)

#     def test_temperature_field_required(self):
#         with self.assertRaises(ValueError):
#             Weather.objects.create(date="2023-06-21", temperature=0)
            
# Integration Test for Retrieving Weather Data
class WeatherIntegrationTest(TestCase):
    def test_retrieve_weather_data(self):
        Weather.objects.create(date="2023-06-21", temperature=25.5)
        weather = Weather.objects.get(date="2023-06-21")
        self.assertEqual(weather.temperature, 25.5)