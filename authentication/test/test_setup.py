from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from faker import Faker
# import pdb

class TestSetup(APITestCase):
    
    def setUp(self):
      self.register_url = reverse('register')
      self.login_url = reverse('login')
      self.fake = Faker()

      self.user_data={
        'email': self.fake.email(),
        'username': self.fake.email().split('@')[0],
        'password': 'Hola2022@',
      }

      return super().setUp()

    def tearDown(self):
      # self.register_url = reverse('register')
      # self.login_url = reverse('login')
      return super().tearDown()