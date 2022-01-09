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

    
    
#test de la función de postproc Bipartitanship, 
#comprueba que las dos opciones mayoritarias obtienen 25 y 15 escaños cada una
    def test_bipartitanship(self):
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
            { 'option': 'Option 3', 'number': 3, 'votes': 30, 'postproc': 15 },
            { 'option': 'Option 4', 'number': 4, 'votes': 20, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_bipartitanship2(self):
            data = {
            'type': 'BIPARTITANSHIP',
            'numEscanyos': 30,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 40 },
                { 'option': 'Option 2', 'number': 2, 'votes': 5 },
                { 'option': 'Option 3', 'number': 3, 'votes': 20 },
                { 'option': 'Option 4', 'number': 4, 'votes': 10 },
            ]
        }

            expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 40, 'postproc': 20 },
            { 'option': 'Option 3', 'number': 3, 'votes': 20, 'postproc': 10 },
            { 'option': 'Option 4', 'number': 4, 'votes': 10, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 5, 'postproc': 0 },
        ]
            response = self.client.post('/postproc/', data, format='json')
            self.assertEqual(response.status_code, 200)

            values = response.json()
            self.assertEqual(values, expected_result)
    
    def test_bipartitanship3(self):
        data = {
            'type': 'BIPARTITANSHIP',
            'numEscanyos': 50,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 50 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 30 },
                { 'option': 'Option 4', 'number': 4, 'votes': 20 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 50, 'postproc': 31 },
            { 'option': 'Option 3', 'number': 3, 'votes': 30, 'postproc': 19 },
            { 'option': 'Option 4', 'number': 4, 'votes': 20, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]
    def test_bipartitanship4(self):
            data = {
            'type': 'BIPARTITANSHIP',
            'numEscanyos': 60,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 70 },
                { 'option': 'Option 2', 'number': 2, 'votes': 2 },
                { 'option': 'Option 3', 'number': 3, 'votes': 40 },
                { 'option': 'Option 4', 'number': 4, 'votes': 15 },
            ]
        }

            expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 70, 'postproc': 38 },
            { 'option': 'Option 3', 'number': 3, 'votes': 40, 'postproc': 22 },
            { 'option': 'Option 4', 'number': 4, 'votes': 15, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 2, 'postproc': 0 },
        ]    
        
            response = self.client.post('/postproc/', data, format='json')
            self.assertEqual(response.status_code, 200)

            values = response.json()
            self.assertEqual(values, expected_result)   
            
    def test_bipartitanship5(self):
            data = {
            'type': 'BIPARTITANSHIP',
            'numEscanyos': 10,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 70 },
                { 'option': 'Option 2', 'number': 2, 'votes': 2 },
                { 'option': 'Option 3', 'number': 3, 'votes': 40 },
                { 'option': 'Option 4', 'number': 4, 'votes': 15 },
            ]
        }

            expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 70, 'postproc': 6 },
            { 'option': 'Option 3', 'number': 3, 'votes': 40, 'postproc': 4 },
            { 'option': 'Option 4', 'number': 4, 'votes': 15, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 2, 'postproc': 0 },
        ]    
        
            response = self.client.post('/postproc/', data, format='json')
            self.assertEqual(response.status_code, 200)

            values = response.json()
            self.assertEqual(values, expected_result)

    def test_bipartitanship6(self):
            data = {
            'type': 'BIPARTITANSHIP',
            'numEscanyos': 100,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 100000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 80000 },
                { 'option': 'Option 3', 'number': 3, 'votes': 30000 },
                { 'option': 'Option 4', 'number': 4, 'votes': 20000 },
            ]
        }

            expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 100000, 'postproc': 56 },
            { 'option': 'Option 2', 'number': 2, 'votes': 80000, 'postproc': 44 },
            { 'option': 'Option 3', 'number': 3, 'votes': 30000, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 20000, 'postproc': 0 },
        ]    
        
            response = self.client.post('/postproc/', data, format='json')
            self.assertEqual(response.status_code, 200)

            values = response.json()
            self.assertEqual(values, expected_result)      


    def test_bipartitanship7(self):
            data = {
            'type': 'BIPARTITANSHIP',
            'numEscanyos': 500,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 55000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 25000 },
                { 'option': 'Option 3', 'number': 3, 'votes': 22000 },
                { 'option': 'Option 4', 'number': 4, 'votes': 15000 },
            ]
        }

            expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 55000, 'postproc': 344 },
            { 'option': 'Option 2', 'number': 2, 'votes': 25000, 'postproc': 156 },
            { 'option': 'Option 3', 'number': 3, 'votes': 22000, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 15000, 'postproc': 0 },
        ]    
        
            response = self.client.post('/postproc/', data, format='json')
            self.assertEqual(response.status_code, 200)

            values = response.json()
            self.assertEqual(values, expected_result)     
            
    def test_bipartitanship8(self):
            data = {
            'type': 'BIPARTITANSHIP',
            'numEscanyos': 0,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 50000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 20000 },
                { 'option': 'Option 3', 'number': 3, 'votes': 10000 },
                { 'option': 'Option 4', 'number': 4, 'votes': 5000 },
            ]
        }
            expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 50000, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 20000, 'postproc': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 10000, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 5000, 'postproc': 0 },
        ]            
            response = self.client.post('/postproc/', data, format='json')
            self.assertEqual(response.status_code, 200)

            values = response.json()
            self.assertEqual(values, expected_result)          
             
    def test_bipartitanshipSinEscaños(self):
            data = {
            'type': 'BIPARTITANSHIP',
            'numEscanyos': 0,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 55 },
                { 'option': 'Option 2', 'number': 2, 'votes': 25 },
                { 'option': 'Option 3', 'number': 3, 'votes': 22 },
                { 'option': 'Option 4', 'number': 4, 'votes': 12 },
            ]
        }

            expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 55, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 25, 'postproc': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 22, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 12, 'postproc': 0 },
        ]    
        
            response = self.client.post('/postproc/', data, format='json')
            self.assertEqual(response.status_code, 200)

            values = response.json()
            self.assertEqual(values, expected_result)   
   
    def test_hamilton(self):   
        data = {
            'type': 'HAMILTON',
            'options': [
                {'option':'A','number':1,'votes': 100000},
                {'option':'B', 'number':2,'votes': 80000},
                {'option':'C', 'number':3,'votes': 30000},
                {'option':'D', 'number':4,'votes': 20000}
            ], 'numEscanyos': 10

        }

        expected_result = [
            {'option':'A','number':1,'votes': 100000, 'postproc': 4},
            {'option':'B', 'number':2,'votes': 80000, 'postproc': 4},
            {'option':'C', 'number':3,'votes': 30000, 'postproc': 1},
            {'option':'D', 'number':4,'votes': 20000, 'postproc': 1}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

       
    def test_hamilton2(self):   
        data = {
            'type': 'HAMILTON',
            'options': [
                {'option':'A','number':1,'votes': 100000},
                {'option':'B', 'number':2,'votes': 80000},
                {'option':'C', 'number':3,'votes': 30000},
                {'option':'D', 'number':4,'votes': 20000}
            ], 'numEscanyos': 80

        }

        expected_result = [
            {'option':'A','number':1,'votes': 100000, 'postproc': 35},
            {'option':'B', 'number':2,'votes': 80000, 'postproc': 28},
            {'option':'C', 'number':3,'votes': 30000, 'postproc': 10},
            {'option':'D', 'number':4,'votes': 20000, 'postproc': 7}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

         
    def test_hamilton3(self):   
        data = {
            'type': 'HAMILTON',
            'options': [
                {'option':'A','number':1,'votes': 100},
                {'option':'B', 'number':2,'votes': 800},
                {'option':'C', 'number':3,'votes': 30},
                {'option':'D', 'number':4,'votes': 20}
            ], 'numEscanyos': 20

        }

        expected_result = [
            {'option':'A','number':1,'votes': 100, 'postproc':2},
            {'option':'B', 'number':2,'votes': 800, 'postproc': 17},
            {'option':'C', 'number':3,'votes': 30, 'postproc': 1},
            {'option':'D', 'number':4,'votes': 20, 'postproc': 0}
        ]
    def test_hamilton4(self):   
        data = {
            'type': 'HAMILTON',
            'options': [
                {'option':'A','number':1,'votes': 10000000000},
                {'option':'B', 'number':2,'votes': 80},
                {'option':'C', 'number':3,'votes': 30},
                {'option':'D', 'number':4,'votes': 20}
            ], 'numEscanyos': 4

        }

        expected_result = [
            {'option':'A','number':1,'votes': 10000000000, 'postproc':4},
            {'option':'B', 'number':2,'votes': 80, 'postproc': 0},
            {'option':'C', 'number':3,'votes': 30, 'postproc': 0},
            {'option':'D', 'number':4,'votes': 20, 'postproc': 0}
        ]
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
        
    def test_hamilton5(self):   
        data = {
            'type': 'HAMILTON',
            'options': [
                {'option':'A','number':1,'votes': 10000000000},
                {'option':'B', 'number':2,'votes': 8000},
                {'option':'C', 'number':3,'votes': 30005},
                {'option':'D', 'number':4,'votes': 201}
            ], 'numEscanyos': 100

        }

        expected_result = [
            {'option':'A','number':1,'votes': 10000000000, 'postproc':100},
            {'option':'B', 'number':2,'votes': 8000, 'postproc': 0},
            {'option':'C', 'number':3,'votes': 30005, 'postproc': 0},
            {'option':'D', 'number':4,'votes': 201, 'postproc': 0}
        ]
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result) 

    def test_hamiltonSinEscaños(self):
            data = {
            'numEscanyos': 0,
            'type': 'HAMILTON',
            'options': [
                {'option':'A','number':1,'votes': 10000},
                {'option':'B', 'number':2,'votes': 8000},
                {'option':'C', 'number':3,'votes': 3000},
                {'option':'D', 'number':4,'votes': 200}
            ]
        }

            expected_result = [
            {'option':'A','number':1,'votes': 10000, 'postproc':0},
            {'option':'B', 'number':2,'votes': 8000, 'postproc': 0},
            {'option':'C', 'number':3,'votes': 3000, 'postproc': 0},
            {'option':'D', 'number':4,'votes': 200, 'postproc': 0}
        ]    
        
            response = self.client.post('/postproc/', data, format='json')
            self.assertEqual(response.status_code, 200)

            values = response.json()
            self.assertEqual(values, expected_result)          
             
    def test_hamilton6(self):
            data = {
            'type': 'HAMILTON',
            'numEscanyos': 0,
            'options': [
                {'option':'A','number':1,'votes': 1000},
                {'option':'B', 'number':2,'votes': 8000},
                {'option':'C', 'number':3,'votes': 300},
                {'option':'D', 'number':4,'votes': 201}
            ]
        }

            expected_result = [
            {'option':'A','number':1,'votes': 1000, 'postproc':0},
            {'option':'B', 'number':2,'votes': 8000, 'postproc': 0},
            {'option':'C', 'number':3,'votes': 300, 'postproc': 0},
            {'option':'D', 'number':4,'votes': 201, 'postproc': 0}
        ]    
        
            response = self.client.post('/postproc/', data, format='json')
            self.assertEqual(response.status_code, 200)

            values = response.json()
            self.assertEqual(values, expected_result)   
    
    def test_hamiltonVotosNegativos(self):   
        data = {
            'type': 'HAMILTON',
            'options': [
                {'option':'A','number':1,'votes': -10000},
                {'option':'B', 'number':2,'votes': -8000},
                {'option':'C', 'number':3,'votes': -3000},
                {'option':'D', 'number':4,'votes': -200}
            ], 'numEscanyos': 250

        }

        expected_result = [
            {'option':'A','number':1,'votes': -10000, 'postproc':0},
            {'option':'B', 'number':2,'votes': -8000, 'postproc': 0},
            {'option':'C', 'number':3,'votes': -3000, 'postproc': 0},
            {'option':'D', 'number':4,'votes': -200, 'postproc': 0}
        ]
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result) 

    def test_hamiltonEscañosNegativos(self):   
        data = {
            'type': 'HAMILTON',
            'options': [
                {'option':'A','number':1,'votes': 100000},
                {'option':'B', 'number':2,'votes': 80000},
                {'option':'C', 'number':3,'votes': 30000},
                {'option':'D', 'number':4,'votes': 20000}
            ], 'numEscanyos': -10

        }

        expected_result = [
            {'option':'A','number':1,'votes': 100000, 'postproc': 0},
            {'option':'B', 'number':2,'votes': 80000, 'postproc': 0},
            {'option':'C', 'number':3,'votes': 30000, 'postproc': 0},
            {'option':'D', 'number':4,'votes': 20000, 'postproc': 0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

#test de la función de postproc HuntingtonHill, 

    def testHuntington(self):   
        data = {
            'type': 'HUNTINGTONHILL', 
            'options': [
        {'option':'A','number':1,'votes': 95000},
        {'option':'B', 'number':2,'votes': 75000},
        {'option':'C', 'number':3,'votes': 25000},
        {'option':'D', 'number':4,'votes': 15000}
        ], 'numEscanyos': 8

        }

        expected_result = [
        {'option':'A','number':1,'votes': 95000,'postproc':4}, 
        {'option':'B', 'number':2,'votes': 75000,'postproc':3}, 
        {'option':'C', 'number':3,'votes': 25000,'postproc':1},
        {'option':'D', 'number':4,'votes': 15000,'postproc':0}
]
        response = self.client.post('/postproc/', data, format='json') 

        self.assertEqual(response.status_code, 200)
        values = response.json()


        self.assertEqual(values, expected_result)
        
    def testHuntington2(self):   
        data = {
            'type': 'HUNTINGTONHILL', 
            'options': [
        {'option':'A','number':1,'votes': 100000},
        {'option':'B', 'number':2,'votes': 8000},
        {'option':'C', 'number':3,'votes': 2500},
        {'option':'D', 'number':4,'votes': 150}
        ], 'numEscanyos': 100

        }

        expected_result = [
        {'option':'A','number':1,'votes': 100000,'postproc':91}, 
        {'option':'B', 'number':2,'votes': 8000,'postproc':7}, 
        {'option':'C', 'number':3,'votes': 2500,'postproc':2},
        {'option':'D', 'number':4,'votes': 150,'postproc':0}
        
]
        response = self.client.post('/postproc/', data, format='json') 
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)
     

    def testHuntington3(self):   
        data = {
            'type': 'HUNTINGTONHILL', 
            'options': [
        {'option':'A','number':1,'votes': 100000},
        {'option':'B', 'number':2,'votes': 8000},
        {'option':'C', 'number':3,'votes': 2500},
        {'option':'D', 'number':4,'votes': 150}
        ], 'numEscanyos': 50

        }

        expected_result = [
        {'option':'A','number':1,'votes': 100000,'postproc':45}, 
        {'option':'B', 'number':2,'votes': 8000,'postproc':4}, 
        {'option':'C', 'number':3,'votes': 2500,'postproc':1},
        {'option':'D', 'number':4,'votes': 150,'postproc':0}
        
]
        response = self.client.post('/postproc/', data, format='json') 

        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)
    
    def testHuntington4GrandesDatos(self):   
        data = {
            'type': 'HUNTINGTONHILL', 
            'options': [
        {'option':'A','number':1,'votes': 10000000},
        {'option':'B', 'number':2,'votes': 800000},
        {'option':'C', 'number':3,'votes': 25000000},
        {'option':'D', 'number':4,'votes': 1500000}
        ], 'numEscanyos': 1000

        }

        expected_result = [
            {'option':'A','number':1,'votes': 10000000,'postproc':268}, 
        {'option':'B', 'number':2,'votes': 800000,'postproc':21}, 
        {'option':'C', 'number':3,'votes': 25000000,'postproc':671},
        {'option':'D', 'number':4,'votes': 1500000,'postproc':40}
        
]
        response = self.client.post('/postproc/', data, format='json') 

        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def testHuntington5PequeñosDatos(self):   
        data = {
            'type': 'HUNTINGTONHILL', 
            'options': [
        {'option':'A','number':1,'votes': 4},
        {'option':'B', 'number':2,'votes': 3},
        {'option':'C', 'number':3,'votes': 2},
        {'option':'D', 'number':4,'votes': 1}
        ], 'numEscanyos': 3

        }

        expected_result = [
            {'option':'A','number':1,'votes': 4,'postproc':2}, 
        {'option':'B', 'number':2,'votes': 3,'postproc':1}, 
        {'option':'C', 'number':3,'votes': 2,'postproc':0},
        {'option':'D', 'number':4,'votes': 1,'postproc':0}
        
]
        response = self.client.post('/postproc/', data, format='json') 

        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def testHuntington6(self):   
        data = {
            'type': 'HUNTINGTONHILL', 
            'options': [
        {'option':'A','number':1,'votes': 100000},
        {'option':'B', 'number':2,'votes': 80000},
        {'option':'C', 'number':3,'votes': 30000},
        {'option':'D', 'number':4,'votes': 20000}
        ], 'numEscanyos': 60

        }

        expected_result = [
        {'option':'A','number':1,'votes': 100000,'postproc':26}, 
        {'option':'B', 'number':2,'votes': 80000,'postproc':21}, 
        {'option':'C', 'number':3,'votes': 30000,'postproc':8},
        {'option':'D', 'number':4,'votes': 20000,'postproc':5}
        
]
        response = self.client.post('/postproc/', data, format='json') 

        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def testHuntington7(self):   
        data = {
            'type': 'HUNTINGTONHILL', 
            'options': [
        {'option':'A','number':1,'votes': 12300},
        {'option':'B', 'number':2,'votes': 81000},
        {'option':'C', 'number':3,'votes': 200},
        {'option':'D', 'number':4,'votes': 10}
        ], 'numEscanyos': 200

        }

        expected_result = [
        {'option':'A','number':1,'votes': 12300,'postproc':26}, 
        {'option':'B', 'number':2,'votes': 81000,'postproc':174}, 
        {'option':'C', 'number':3,'votes': 200,'postproc':0},
        {'option':'D', 'number':4,'votes': 10,'postproc':0}
        
]
        response = self.client.post('/postproc/', data, format='json') 

        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def testHuntingtonSinEscaños(self):   
        data = {
            'type': 'HUNTINGTONHILL', 
            'options': [
        {'option':'A','number':1,'votes': 12000},
        {'option':'B', 'number':2,'votes': 8000},
        {'option':'C', 'number':3,'votes': 200},
        {'option':'D', 'number':4,'votes': 10}
        ], 'numEscanyos': 0

        }

        expected_result = [
        {'option':'A','number':1,'votes': 12000,'postproc':0}, 
        {'option':'B', 'number':2,'votes': 8000,'postproc':0}, 
        {'option':'C', 'number':3,'votes': 200,'postproc':0},
        {'option':'D', 'number':4,'votes': 10,'postproc':0}
        
]
        response = self.client.post('/postproc/', data, format='json') 

        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def testHuntingtonVotosNegativos(self):   
        data = {
            'type': 'HUNTINGTONHILL', 
            'options': [
        {'option':'A','number':1,'votes': -12000},
        {'option':'B', 'number':2,'votes': -8000},
        {'option':'C', 'number':3,'votes': -200},
        {'option':'D', 'number':4,'votes': -10}
        ], 'numEscanyos': 250

        }

        expected_result = [
        {'option':'A','number':1,'votes': -12000,'postproc':0}, 
        {'option':'B', 'number':2,'votes': -8000,'postproc':0}, 
        {'option':'C', 'number':3,'votes': -200,'postproc':0},
        {'option':'D', 'number':4,'votes': -10,'postproc':0}
        
]
        response = self.client.post('/postproc/', data, format='json') 

        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def testHuntingtonEscañosNegativos(self):   
        data = {
            'type': 'HUNTINGTONHILL', 
            'options': [
        {'option':'A','number':1,'votes': 95000},
        {'option':'B', 'number':2,'votes': 75000},
        {'option':'C', 'number':3,'votes': 25000},
        {'option':'D', 'number':4,'votes': 15000}
        ], 'numEscanyos': -8

        }

        expected_result = [
        {'option':'A','number':1,'votes': 95000,'postproc':0}, 
        {'option':'B', 'number':2,'votes': 75000,'postproc':0}, 
        {'option':'C', 'number':3,'votes': 25000,'postproc':0},
        {'option':'D', 'number':4,'votes': 15000,'postproc':0}
]
        response = self.client.post('/postproc/', data, format='json') 

        self.assertEqual(response.status_code, 200)
        values = response.json()


        self.assertEqual(values, expected_result)

  #test de la función de postproc DHont,       

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
            'numEscanyos': 10
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
            'numEscanyos': 10
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
            'numEscanyos': 100
        }

        expected_result = [
            {'option':'Option 1','number':1,'votes': 65000,'postproc': 65},
            {'option':'Option 2','number':2,'votes': 30000,'postproc': 29},
            {'option':'Option 3','number':3,'votes': 1500,'postproc': 1},
            {'option':'Option 4','number':4,'votes': 4500,'postproc': 4},
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
            'numEscanyos': 300
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
            'numEscanyos': 100
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

    
    def testDHont6(self): #Escaños elevados
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'Option 1','number':1,'votes': 15000},
                {'option':'Option 2','number':2,'votes': 75000},
                {'option':'Option 3','number':3,'votes': 10000},
                {'option':'Option 4','number':4,'votes': 5000},
                {'option':'Option 5','number':5,'votes': 2500},
            ],
            'numEscanyos': 900
        }

        expected_result = [
            {'option':'Option 1','number':1,'votes': 15000,'postproc': 126},
            {'option':'Option 2','number':2,'votes': 75000,'postproc': 630},
            {'option':'Option 3','number':3,'votes': 10000,'postproc': 83},
            {'option':'Option 4','number':4,'votes': 5000,'postproc': 41},
            {'option':'Option 5','number':5,'votes': 2500,'postproc': 20}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def testDHont7(self): #Número de votos iguales.
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'OPT1','number':1,'votes': 50000},
                {'option':'OPT2','number':2,'votes': 50000}
            ],
            'numEscanyos': 20
        }

        expected_result = [
            {'option':'OPT1','number':1,'votes': 50000,'postproc': 10},
            {'option':'OPT2','number':2,'votes': 50000,'postproc': 10}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)  


        
    def testDHont8(self): 
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'Option 1','number':1,'votes': 2000},
                {'option':'Option 2','number':2,'votes': 3000},
                {'option':'Option 3','number':3,'votes': 4500},
                {'option':'Option 4','number':4,'votes': 5000},
                {'option':'Option 5','number':5,'votes': 2500},
            ],
            'numEscanyos': 1000
        }

        expected_result = [
            {'option':'Option 1','number':1,'votes': 2000,'postproc': 118},
            {'option':'Option 2','number':2,'votes': 3000,'postproc': 176},
            {'option':'Option 3','number':3,'votes': 4500,'postproc': 265},
            {'option':'Option 4','number':4,'votes': 5000,'postproc': 294},
            {'option':'Option 5','number':5,'votes': 2500,'postproc': 147}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def testDHont9(self): 
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'Option 1','number':1,'votes': 100000},
                {'option':'Option 2', 'number':2,'votes': 80000},
                {'option':'Option 3', 'number':3,'votes': 30000},
                {'option':'Option 4', 'number':4,'votes': 20000}
            ],
            'numEscanyos': 60
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'votes': 100000, 'postproc': 26},
            {'option': 'Option 2', 'number': 2, 'votes': 80000, 'postproc': 21},
            {'option': 'Option 3', 'number': 3, 'votes': 30000, 'postproc': 8},
            {'option': 'Option 4', 'number': 4, 'votes': 20000, 'postproc': 5}
            ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def testDHontSinEscaños(self): 
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'Option 1','number':1,'votes': 2000},
                {'option':'Option 2','number':2,'votes': 3000},
                {'option':'Option 3','number':3,'votes': 4500},
                {'option':'Option 4','number':4,'votes': 5000},
                {'option':'Option 5','number':5,'votes': 2500},
            ],
            'numEscanyos': 0
        }

        expected_result = [
            {'option':'Option 1','number':1,'votes': 2000,'postproc': 0},
            {'option':'Option 2','number':2,'votes': 3000,'postproc': 0},
            {'option':'Option 3','number':3,'votes': 4500,'postproc': 0},
            {'option':'Option 4','number':4,'votes': 5000,'postproc': 0},
            {'option':'Option 5','number':5,'votes': 2500,'postproc': 0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def testDHontEscañosNegativos(self): #Fácil de comprobar manualmente
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
            'numEscanyos': -10
        }

        expected_result = [
            {'option':'Option 1','number':1,'votes': 12000, 'postproc': 0},
            {'option':'Option 2','number':2,'votes': 140000, 'postproc': 0},
            {'option':'Option 3','number':3,'votes': 110000, 'postproc': 0},
            {'option':'Option 4','number':4,'votes': 205000, 'postproc': 0},
            {'option':'Option 5','number':5,'votes': 150000, 'postproc': 0},
            {'option':'Option 6','number':6,'votes': 16000, 'postproc': 0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result) 


    #test de la función de postproc Imperiali, 

    def test_imperiali(self):
        data={
        'type':'IMPERIALI',
        'options':[

            {'option':'A', 'number':1, 'votes':391000},
            {'option':'B', 'number':2, 'votes':311000},
            {'option':'C', 'number':2, 'votes':184000},
            {'option':'D', 'number':4, 'votes':73000},
            {'option':'E', 'number':5, 'votes':27000},
            {'option':'F', 'number':6, 'votes':12000},
            {'option':'G', 'number':7, 'votes':2000},

        ], 
        'numEscanyos':21


        }

        expected_result=[
            {'option':'A', 'number':1, 'votes':391000, 'postproc':9},
            {'option':'B', 'number':2, 'votes':311000, 'postproc':7},
            {'option':'C', 'number':2, 'votes':184000, 'postproc':4},
            {'option':'D', 'number':4, 'votes':73000, 'postproc':1},
            {'option':'E', 'number':5, 'votes':27000, 'postproc':0},
            {'option':'F', 'number':6, 'votes':12000, 'postproc':0},
            {'option':'G', 'number':7, 'votes':2000, 'postproc':0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
        

    def test_imperiali2(self):
        data={
        'type':'IMPERIALI',
        'options':[

            {'option':'A', 'number':1, 'votes':1000},
            {'option':'B', 'number':2, 'votes':2000},
            {'option':'C', 'number':3, 'votes':400},
            {'option':'D', 'number':4, 'votes':30}
        ], 
        'numEscanyos':300


        }

        expected_result=[
            {'option':'B', 'number':2, 'votes':2000, 'postproc':181},
            {'option':'A', 'number':1, 'votes':1000, 'postproc':90},
            {'option':'C', 'number':3, 'votes':400, 'postproc':36},
            {'option':'D', 'number':4, 'votes':30, 'postproc':2}
        ]

#test Imperiali con 0 escaños a repartir
    def test_imperiali3(self):
        data={
        'type':'IMPERIALI',
        'options':[

            {'option':'A', 'number':1, 'votes':10},
            {'option':'B', 'number':2, 'votes':20},
            {'option':'C', 'number':3, 'votes':5},
            {'option':'D', 'number':4, 'votes':6}
        ], 
        'numEscanyos':0
        }

        expected_result = [
            {'option':'A', 'number':1, 'votes':10, 'postproc':0},
            {'option':'B', 'number':2, 'votes':20, 'postproc':0},
            {'option':'C', 'number':3, 'votes':5, 'postproc':0},
            {'option':'D', 'number':4, 'votes':6, 'postproc':0}
        ]
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

#test de la función de postproc SainteLague, 

    def test_saintelague1(self):
        data = {
                'type': 'SAINTELAGUE',
                'numEscanyos': 40,
                'options': [
                    { 'option': 'Option 1', 'number': 1, 'votes': 1200 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 700 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 650 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 400 },
                    { 'option': 'Option 5', 'number': 5, 'votes': 200 },
                ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 1200, 'postproc': 15 },
            { 'option': 'Option 2', 'number': 2, 'votes': 700, 'postproc': 9 },
            { 'option': 'Option 3', 'number': 3, 'votes': 650, 'postproc': 8 },
            { 'option': 'Option 4', 'number': 4, 'votes': 400, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 200, 'postproc': 3 }
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)
        
    def test_saintelague2(self):
        data = {
                'type': 'SAINTELAGUE',
                'numEscanyos': 40,
                'options': [
                    { 'option': 'Option 1', 'number': 1, 'votes': 12000 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 7000 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 6500 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 4000 },
                    { 'option': 'Option 5', 'number': 5, 'votes': 2000 },
                ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 12000, 'postproc': 15 },
            { 'option': 'Option 2', 'number': 2, 'votes': 7000, 'postproc': 9 },
            { 'option': 'Option 3', 'number': 3, 'votes': 6500, 'postproc': 8 },
            { 'option': 'Option 4', 'number': 4, 'votes': 4000, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 2000, 'postproc': 3 }
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def test_saintelague3(self):
        data = {
                'type': 'SAINTELAGUE',
                'numEscanyos': 4,
                'options': [
                    { 'option': 'Option 1', 'number': 1, 'votes': 1200 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 700 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 650 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 400 },
                    { 'option': 'Option 5', 'number': 5, 'votes': 200 },
                ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 1200, 'postproc': 2 },
            { 'option': 'Option 2', 'number': 2, 'votes': 700, 'postproc': 1 },
            { 'option': 'Option 3', 'number': 3, 'votes': 650, 'postproc': 1 },
            { 'option': 'Option 4', 'number': 4, 'votes': 400, 'postproc': 0 },
            { 'option': 'Option 5', 'number': 5, 'votes': 200, 'postproc': 0 }
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def test_saintelague4GrandesDatos(self):
        data = {
                'type': 'SAINTELAGUE',
                'numEscanyos': 400,
                'options': [
                    { 'option': 'Option 1', 'number': 1, 'votes': 100000 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 50000 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 25000 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 1000 },
                    { 'option': 'Option 5', 'number': 5, 'votes': 105 },
                ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 100000, 'postproc': 227 },
            { 'option': 'Option 2', 'number': 2, 'votes': 50000, 'postproc': 114},
            { 'option': 'Option 3', 'number': 3, 'votes': 25000, 'postproc': 57 },
            { 'option': 'Option 4', 'number': 4, 'votes': 1000, 'postproc': 2 },
            { 'option': 'Option 5', 'number': 5, 'votes': 105, 'postproc': 0 }
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)
    def test_saintelague5PequeñosDatos(self):
        data = {
                'type': 'SAINTELAGUE',
                'numEscanyos': 6,
                'options': [
                    { 'option': 'Option 1', 'number': 1, 'votes': 6 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 4 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 2 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 1 },
                    { 'option': 'Option 5', 'number': 5, 'votes': 0 },
                ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 6, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 4, 'postproc': 0},
            { 'option': 'Option 3', 'number': 3, 'votes': 2, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 1, 'postproc': 0},
            { 'option': 'Option 5', 'number': 5, 'votes': 0, 'postproc': 0 }
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)


    def test_saintelague6(self):
        data = {
            'type': 'SAINTELAGUE',
            'numEscanyos': 5,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 20 },
                { 'option': 'Option 2', 'number': 2, 'votes': 60 },
                { 'option': 'Option 3', 'number': 3, 'votes': 10 },
            ]
        }

        expected_result = [
            { 'option': 'Option 2', 'number': 2, 'votes': 60, 'postproc': 3 },
            { 'option': 'Option 1', 'number': 1, 'votes': 20, 'postproc': 1 },
            { 'option': 'Option 3', 'number': 3, 'votes': 10, 'postproc': 1 }

        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    


    def test_saintelague7(self):
        data = {
            'type': 'SAINTELAGUE',
            'numEscanyos': 0,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 1000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 800 },
                { 'option': 'Option 3', 'number': 3, 'votes': 750 },
                { 'option': 'Option 4', 'number': 4, 'votes': 600 },
                { 'option': 'Option 5', 'number': 5, 'votes': 350 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 1000, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 800, 'postproc': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 750, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 600, 'postproc': 0 },
            { 'option': 'Option 5', 'number': 5, 'votes': 350, 'postproc': 0 }
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)



    def test_saintelague8(self):
        data = {
            'type': 'SAINTELAGUE',
            'numEscanyos': 0,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 0 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 0 },
                { 'option': 'Option 4', 'number': 4, 'votes': 0 },
                { 'option': 'Option 5', 'number': 5, 'votes': 0 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 5', 'number': 5, 'votes': 0, 'postproc': 0 }
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)



    def test_saintelague9(self):
        data = {
            'type': 'SAINTELAGUE',
            'numEscanyos': -4,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 1000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 800 },
                { 'option': 'Option 3', 'number': 3, 'votes': 750 },
                { 'option': 'Option 4', 'number': 4, 'votes': 600 },
                { 'option': 'Option 5', 'number': 5, 'votes': 350 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 1000, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 800, 'postproc': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 750, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 600, 'postproc': 0 },
            { 'option': 'Option 5', 'number': 5, 'votes': 350, 'postproc': 0 }
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)



    def test_saintelague10(self):
        data = {
            'type': 'SAINTELAGUE',
            'numEscanyos': 8,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 10 },
                { 'option': 'Option 2', 'number': 2, 'votes':5 }
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 10, 'postproc': 5 },
            { 'option': 'Option 2', 'number': 2, 'votes': 5, 'postproc':3  }
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_saintelague11(self):
            data = {
                'type': 'SAINTELAGUE',
                'numEscanyos': 20,
                'options': [
                    { 'option': 'Option 2', 'number': 1, 'votes': 100000 },
                    { 'option': 'Option 1', 'number': 2, 'votes':250000 }
                ]
            }

            expected_result = [
                { 'option': 'Option 1', 'number': 2, 'votes': 250000, 'postproc': 14 }, 
                { 'option': 'Option 2', 'number': 1, 'votes': 100000, 'postproc': 6 }
            ]
            
            response = self.client.post('/postproc/', data, format='json')
            self.assertEqual(response.status_code, 200)

            values = response.json()
            self.assertEqual(values, expected_result)


    def test_saintelague12(self):
            data = {
                'type': 'SAINTELAGUE',
                'numEscanyos': 20,
                'options': [
                {'option':'Option 1','number':1,'votes': 100000},
                {'option':'Option 2', 'number':2,'votes': 80000},
                {'option':'Option 3', 'number':3,'votes': 30000},
                {'option':'Option 4', 'number':4,'votes': 20000}
            ],
            'numEscanyos': 60
        }

            expected_result = [
                {'option': 'Option 1', 'number': 1, 'votes': 100000, 'postproc': 26},
                {'option': 'Option 2', 'number': 2, 'votes': 80000, 'postproc': 21},
                {'option': 'Option 3', 'number': 3, 'votes': 30000, 'postproc': 8},
                {'option': 'Option 4', 'number': 4, 'votes': 20000, 'postproc': 5}
            ]
            
            response = self.client.post('/postproc/', data, format='json')
            self.assertEqual(response.status_code, 200)

            values = response.json()
            self.assertEqual(values, expected_result)
