import unittest
import models
from app import app


class TodoTests(unittest.TestCase):
    """Todo Tests"""

    def setUp(self):
        models.initialize()
        self.app = app.test_client()

    def tearDown(self):
        models.DATABASE.drop_tables(models.Todo)
        models.DATABASE.close()

    def test_home(self):
        """Test home"""
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<body ng-app="todoListApp">', str(result.data))

    def test_item(self):
        """Test api endpoints"""
        result = self.app.post('/api/v1/todos', data={'name': 'Test Name',
                                                      'completed': False})
        self.assertEqual(result.status_code, 201)
        query = models.Todo.get(name='Test Name')

        # Item in main list
        result = self.app.get('/api/v1/todos')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Test Name', str(result.data))

        # Get item
        result = self.app.get('/api/v1/todos/{}'.format(query.id))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Test Name', str(result.data))

        # Edit Item
        result = self.app.put('/api/v1/todos/{}'.format(query.id),
                              data={'name': 'Test Name Changed',
                                    'completed': False})
        self.assertIn('/api/v1/todos/{}'.format(query.id),
                      result.headers['location'])
        query = models.Todo.get(name='Test Name Changed')

        # Delete Item
        result = self.app.delete('/api/v1/todos/{}'.format(query.id))
        self.assertEqual(result.status_code, 204)


if __name__ == '__main__':
    unittest.main()
