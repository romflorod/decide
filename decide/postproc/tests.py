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
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_imperiali(self):
        data={
        'type':'IMPERIALI',
        'options':[
            {'option':'A', 'number':1, 'votes':391.000},
            {'option':'B', 'number':2, 'votes':311.000},
            {'option':'C', 'number':2, 'votes':184.000},
            {'option':'D', 'number':4, 'votes':73.000},
            {'option':'E', 'number':5, 'votes':27.000},
            {'option':'F', 'number':6, 'votes':12.000},
            {'option':'G', 'number':7, 'votes':2.000},
        ]
        }

        expected_result=[
            {'option':'A', 'number':1, 'votes':391.000, 'postproc':9},
            {'option':'B', 'number':2, 'votes':311.000, 'postproc':7},
            {'option':'C', 'number':2, 'votes':184.000, 'postproc':4},
            {'option':'D', 'number':4, 'votes':73.000, 'postproc':1},
            {'option':'E', 'number':5, 'votes':27.000, 'postproc':0},
            {'option':'F', 'number':6, 'votes':12.000, 'postproc':0},
            {'option':'G', 'number':7, 'votes':2.000, 'postproc':0},
        ]
    
