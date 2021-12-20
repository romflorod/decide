from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'BIPARTITANSHIP',
            'numEscanyos': 40,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 50 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 30 },
                { 'option': 'Option 4', 'number': 4, 'votes': 20 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 50, 'postproc': 25 },
            { 'option': 'Option 5', 'number': 3, 'votes': 30, 'postproc': 15 },
            { 'option': 'Option 3', 'number': 4, 'votes': 20, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
