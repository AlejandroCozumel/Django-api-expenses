import pdb
from .test_setup import TestSetup
from ..models import User

class TestViews(TestSetup):
  def test_user_cannot_register_with_no_data(self):
    res=self.client.post(self.register_url)
    self.assertEqual(res.status_code, 400) ## check if the status code is 400

  def test_user_can_register_correctly(self):
    res=self.client.post(self.register_url, self.user_data, format="json")
    self.assertEqual(res.data['email'], self.user_data['email']) ## check if the email is the same
    self.assertEqual(res.data['username'], self.user_data['username']) ## check if the username is the same
    self.assertEqual(res.status_code, 201) ## check if the status code is 201

  def test_user_cannot_login_unverify_email(self):
    self.client.post(self.register_url, self.user_data, format="json") ## register the user
    res=self.client.post(self.login_url, self.user_data, format="json") ## login the user
    self.assertEqual(res.status_code, 401) ## check if the status code is 401


  def test_user_can_login_verify_email(self):
    response=self.client.post(self.register_url, self.user_data, format="json") ## register the user
    email=response.data['email'] ## get the email from the response
    user=User.objects.get(email=email) ## get the user from the email
    user.is_verified=True ## set the user to verified
    user.save() ## save the user
    res=self.client.post(self.login_url, self.user_data, format="json") ## login the user
    self.assertEqual(res.status_code, 200) ## check if the status code is 200