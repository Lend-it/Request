import json
import unittest

from datetime import datetime
from project.tests.base import BaseTestCase
from database_singleton import Singleton

db = Singleton().database_connection()


class TestProductCategory(BaseTestCase):
	def test_get_all_category(self):
		with self.client:
			
			self.client.post('/api/product_category',data=json.dumps({
				'name': 'Eletrodomésticos'
			}), content_type='application/json')
			
			self.client.post('/api/product_category',data=json.dumps({
				'name': 'Livros e revistas'
			}), content_type='application/json')

			self.client.post('/api/product_category',data=json.dumps({
				'name': 'Eletrônicos'
			}), content_type='application/json')

			response = self.client.get('/api/product_category')
			data = json.loads(response.data.decode())
			print(data)

			self.assertEqual(response.status_code, 200)
			self.assertIn('success', data['status'])

			self.assertEqual(1, data['data']['categories'][0]['productcategoryid'])
			self.assertIn('Eletrodomésticos', data['data']['categories'][0]['name'])

			self.assertEqual(2, data['data']['categories'][1]['productcategoryid'])
			self.assertIn('Livros e revistas', data['data']['categories'][1]['name'])
			
			self.assertEqual(3, data['data']['categories'][2]['productcategoryid'])
			self.assertIn('Eletrônicos', data['data']['categories'][2]['name'])


if __name__ == '__main__':
	unittest.main()