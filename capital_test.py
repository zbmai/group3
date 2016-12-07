import unittest
from capital import Capital

class TestCapital(unittest.TestCase):
    if __name__ == '__main__':
        unittest.main()

    def setUp(self):
        self.input = self.__get_test_entity()
        self.id = self.input['id']
        self.capital = Capital()

    def tearDown(self):
        try:
            # clean up
            self.capital.delete(self.id)
        except:
            pass

    def test_get(self):
        try:
            entity = self.capital.get(id)
            self.fail("an exception is expected")
        except Exception as ex:
            pass

        try:
            self.capital.insert(id, input)
        except Exception as ex:
            self.fail('failed to insert an entity {}'.format(ex.message))

        entity = self.capital.get(id)
        self.assertEqual(input['name'], entity['name'])
        self.assertEqual(input['countryCode'], entity['countryCode'])
        self.assertEqual(input['country'], entity['country'])
        self.assertEqual(input['id'], entity['id'])
        self.assertEqual(input['continent'], entity['continent'])
        input_location = input['location']
        entity_location = entity['location']
        self.assertEqual(input_location['latitude'], entity_location['latitude'])
        self.assertEqual(input_location['longitude'], entity_location['longitude'])

    def test_get_all(self):
        try:
            self.capital.insert(id, input)
        except Exception as ex:
            self.fail('failed to insert an entity {}'.format(ex.message))

        results = self.capital.get_all()
        self.assertTrue(len(results) > 0)

    def test_insert(self):
        try:
            self.capital.insert(id, input)
        except Exception as ex:
            self.fail('failed to insert an entity {}'.format(ex.message))

    def test_delete(self):
        try:
            self.capital.insert(id, input)
        except Exception as ex:
            self.fail('failed to insert an entity {}'.format(ex.message))

        try:
            self.capital.delete(id)
        except Exception as ex:
            self.fail('failed to delete the created entity {}'.format(ex.message))

    def __get_test_entity(self):
        entity = {}
        location = {}
        entity['location'] = location
        entity['name'] = 'King Edward Point'
        entity['countryCode'] = 'GS'
        entity['country'] = 'South Georgia and South Sandwich Islands'
        entity['id'] = 999999
        entity['continent'] = 'Antarctica'
        location['latitude'] = -54.283333
        location['longitude'] = -36.5
        return entity
