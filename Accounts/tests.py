from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class AccountsTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user(email='test@example.com',
                                                  password='testpassword',
                                                  account_type=1,
                                                  first_name='First Name',
                                                  last_name='Last Name')

        # URL for creating an account.
        self.create_url = reverse('account-create')

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'email': 'foobar@example.com',
            'password': 'somepassword4221AS',
            'account_type': 2,
            'first_name': 'First name',
            'last_name': 'Last name'
        }

        response = self.client.post(self.create_url, data, format='json')

        # We want to make sure we have two users in the database..

        # And that we're returning a 201 created code.

        # Additionally, we want to return the username and email upon successful creation.
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['account_type'], data['account_type'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])

