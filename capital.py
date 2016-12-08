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
            raise Exception('not found')

        results = list(query.fetch())
        if len(results) == 0:
            raise Exception('not found')

        for entity in list(results):
            output = self.__transform(entity, id)
            return output

    def query(self, key, value):
        query = self.ds.query(kind=self.kind)
        query.add_filter(key, '=', value)
        results = list()
        for entity in list(query.fetch()):
            results.append(self.__transform(entity))
        return results

    def search(self, value):
        keys=['id','name','countryCode','country','continent']
        results=list()
        for key in keys:
            sub= self.query(key, value)
            for res in sub:
                results.append(res)
        return results

    def get_all(self):
        query = self.ds.query(kind=self.kind)
        results = list()
        for entity in list(query.fetch()):
            results.append(self.__transform(entity))
        return results

    def get_all_countries(self):
        query = self.ds.query(kind=self.kind)
        results = list()
        resultset = {}
        for entity in list(query.fetch()):
            resultset[entity['country']] = entity
        for key in sorted(resultset):
            results.append(resultset[key])
        return results

    def get_all_max20(self):
        query = self.ds.query(kind=self.kind)
        results = list()
        for entity in list(query.fetch()):
            results.append(self.__transform(entity))
        return results[:20]

    def delete(self, id):
        entity = self.get(id)
        key = self.ds.key(self.kind, id)
        self.ds.delete(key)


    def __transform(self, entity, id=None):
        output = dict()
        location = {}
        if id:
            output['id'] = id
        else:
            output['id'] = entity['id']
        output['name'] = entity['name']
        output['countryCode'] = entity['countryCode']
        output['country'] = entity['country']
        output['continent'] = entity['continent']
        output['location'] = location
        location['latitude'] = entity['location.latitude']
        location['longitude'] = entity['location.longitude']
        return output;
