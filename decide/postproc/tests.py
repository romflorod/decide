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


    def testDHont1(self): #Fácil de comprobar manualmente
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'Option 1','number':1,'votes': 12000},
                {'option':'Option 2','number':2,'votes': 140000},
                {'option':'Option 3','number':3,'votes': 110000},
                {'option':'Option 4','number':4,'votes': 205000},
                {'option':'Option 5','number':5,'votes': 150000},
                {'option':'Option 6','number':6,'votes': 16000}
            ],
            'numEscanos': 10
        }

        expected_result = [
            {'option':'Option 1','number':1,'votes': 12000, 'postproc': 0},
            {'option':'Option 2','number':2,'votes': 140000, 'postproc': 2},
            {'option':'Option 3','number':3,'votes': 110000, 'postproc': 2},
            {'option':'Option 4','number':4,'votes': 205000, 'postproc': 4},
            {'option':'Option 5','number':5,'votes': 150000, 'postproc': 2},
            {'option':'Option 6','number':6,'votes': 16000, 'postproc': 0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result) 


    def testDHont2(self): #Votos muy igualados
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'Option 1','number':1,'votes': 65000},
                {'option':'Option 2','number':2,'votes': 60000},
                {'option':'Option 3','number':3,'votes': 50000},
                {'option':'Option 4','number':4,'votes': 55000},
                {'option':'Option 5','number':5,'votes': 62000},
                {'option':'Option 6','number':6,'votes': 57000},
            ],
            'numEscanos': 10
        }

        expected_result = [
            {'option':'Option 1','number':1,'votes': 65000,'postproc': 2},
            {'option':'Option 2','number':2,'votes': 60000,'postproc': 2},
            {'option':'Option 3','number':3,'votes': 50000,'postproc': 1},
            {'option':'Option 4','number':4,'votes': 55000,'postproc': 1},
            {'option':'Option 5','number':5,'votes': 62000,'postproc': 2},
            {'option':'Option 6','number':6,'votes': 57000,'postproc': 2},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def testDHont3(self): #Votos muy desiguales
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'Option 1','number':1,'votes': 65000},
                {'option':'Option 2','number':2,'votes': 30000},
                {'option':'Option 3','number':3,'votes': 1500},
                {'option':'Option 4','number':4,'votes': 4500},
                {'option':'Option 5','number':5,'votes': 2000},
            ],
            'numEscanos': 100
        }

        expected_result = [
            {'option':'Option 1','number':1,'votes': 65000,'postproc': 32},
            {'option':'Option 2','number':2,'votes': 30000,'postproc': 15},
            {'option':'Option 3','number':3,'votes': 1500,'postproc': 0},
            {'option':'Option 4','number':4,'votes': 4500,'postproc': 2},
            {'option':'Option 5','number':5,'votes': 2000,'postproc': 1},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    
    def testDHont4(self): #Votos iguales
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'Option 1','number':1,'votes': 50000},
                {'option':'Option 2','number':2,'votes': 50000},
                {'option':'Option 3','number':3,'votes': 50000}
            ],
            'numEscanos': 300
        }

        expected_result = [
            {'option':'Option 1','number':1,'votes': 50000,'postproc': 100},
            {'option':'Option 2','number':2,'votes': 50000,'postproc': 100},
            {'option':'Option 3','number':3,'votes': 50000,'postproc': 100}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result) 

    
    def testDHont5(self): #Votos muy elevados
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'Option 1','number':1,'votes': 150150150150150},
                {'option':'Option 2','number':2,'votes': 300300300300300},
                {'option':'Option 3','number':3,'votes': 200200200200200}
            ],
            'numEscanos': 100
        }

        expected_result = [
            {'option':'Option 1','number':1,'votes': 150150150150150,'postproc': 23},
            {'option':'Option 2','number':2,'votes': 300300300300300,'postproc': 46},
            {'option':'Option 3','number':3,'votes': 200200200200200,'postproc': 31}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    
    def testDHont5(self): #Escaños elevados
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'Option 1','number':1,'votes': 15000},
                {'option':'Option 2','number':2,'votes': 75000},
                {'option':'Option 3','number':3,'votes': 10000},
                {'option':'Option 4','number':4,'votes': 5000},
                {'option':'Option 5','number':5,'votes': 2500},
            ],
            'numEscanos': 900
        }

        expected_result = [
            {'option':'Option 1','number':1,'votes': 15000,'postproc': 338},
            {'option':'Option 2','number':2,'votes': 7500,'postproc': 169},
            {'option':'Option 3','number':3,'votes': 10000,'postproc': 225},
            {'option':'Option 4','number':4,'votes': 5000,'postproc': 112},
            {'option':'Option 5','number':5,'votes': 2500,'postproc': 56}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)