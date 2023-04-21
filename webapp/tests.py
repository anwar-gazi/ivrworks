# import unittest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from webapp.forms import AuthForm
from webapp.backends import EmailBackend

formdata = {'email': 'resgef@outlook.com', 'password': '1ta#shobdo'}


def create_test_user():
    get_user_model().objects.create_user(username=formdata['email'], email=formdata['email'],
                                         password=formdata['password'])


# Create your tests here.
class EmailLoginFormTestCase(TestCase):
    def setUp(self) -> None:
        create_test_user()

    def test_usercreate(self):
        created_user = get_user_model().objects.get_by_email(email=formdata['email'])
        self.assertIsNotNone(created_user)

    def test_form_clean(self):
        form = AuthForm(data=formdata)
        form.clean()
        self.assertTrue(form.is_valid())


class EmailBackendTestCase(TestCase):
    def setUp(self) -> None:
        create_test_user()

    def test_user_can_authenticate(self):
        user = get_user_model().objects.get(email=formdata['email'])
        self.assertIsNotNone(EmailBackend().user_can_authenticate(user),
                             f"user cannot authenticate, {formdata['email']}")

    def test_get_user(self):
        self.assertIsNotNone(EmailBackend().get_user(formdata['email']),
                             f"cannot find the user by email {formdata['email']}")

    def test_authenticate(self):
        user = EmailBackend().authenticate(None, email=formdata['email'], password=formdata['password'])
        self.assertIsNotNone(user, "User cannot authenticate")

    def test_authenticated_user_email(self):
        user = EmailBackend().authenticate(None, email=formdata['email'], password=formdata['password'])
        self.assertEquals(user.email, formdata['email'])


class LoginTestCase(TestCase):
    def setUp(self) -> None:
        create_test_user()

    def test_login_statuscode(self):
        c = Client()
        response = c.post('/accounts/login/', formdata, content_type='text/html', follow=True)
        self.assertEquals(response.status_code, 200, f"cannot login")
