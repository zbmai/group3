from google.cloud import datastore
import utility


class Capital:
    def __init__(self):
        self.ds = datastore.Client(project=utility.project_id())
        self.kind = "Capital"

    def insert(self, id, input):
        key = self.ds.key(self.kind, id)
        entity = datastore.Entity(key)

        entity['id'] = id
        entity['name'] = input['name']
        entity['countryCode'] = input['countryCode']
        entity['country'] = input['country']
        entity['continent'] = input['continent']
        location = input.get('location', None)
        if location:
            entity['location.latitude'] = location['latitude']
            entity['location.longitude'] = location['longitude']
        return self.ds.put(entity)

    def get(self, id):
        query = self.ds.query(kind=self.kind)
        query.add_filter('id', '=', id)
        entity = query.fetch()

        if not entity:
            raise 'not found'

        output = dict()
        location = {}

        if len(list(query.fetch())) == 0:
            raise 'not found'

        for entity in list(query.fetch()):
            output['id'] = id
            output['name'] = entity['name']
            output['countryCode'] = entity['countryCode']
            output['country'] = entity['country']
            output['continent'] = entity['continent']
            output['location'] = location
            location['latitude'] = entity['location.latitude']
            location['longitude'] = entity['location.longitude']
            return output


