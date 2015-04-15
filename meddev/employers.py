import json
import re
import requests 
from utils import fieldval, XmlReader




def read_all_pages(url, headers=None):
    while True:
        print url 
        r = requests.get(url, headers=headers)
        resp = json.loads(r.content)

        yield resp['results']
        url = resp.get('next')
        if not url:
            break


class EmpClient(object):

    def __init__(self, url_base, key_secret):
        self.url_base = url_base
        self.key_secret = key_secret
        self.list_url = '{}/app/api/v1/employers/'.format(self.url_base)
        self.quick_list_url = '{}/app/api/v1/employers/quick-list'.format(self.url_base)

    def get_headers(self):
        return {
            'Authentication': 'CL {}'.format(self.key_secret),
            'Content-type': 'application/json'
        }

    def get_existing_ids(self):
        """ returns list of existing old ids in the CL databse,
            so we can skip them during the import 
        """        
        url = '{}?page_size={}'.format(self.quick_list_url, 250)
        headers = self.get_headers()
        ids = []
        for page in read_all_pages(url, headers):
            for item in page:
                old_id = item.get('old_id')
                if old_id:
                    ids.append(int(old_id))
        return ids 

    def save(self, data, id=None):
        headers = self.get_headers()

        if not id:
            url = self.list_url
            # print url, auth
            res = requests.post(url, data=json.dumps(data), headers=headers)
        else:
            raise NotImplementedError("update is not implemented")

        if res.status_code not in [200, 201]: 
            print res.status_code 
            print res.content
        res.raise_for_status()
        print 'saved: {}'.format(data['name'])



class Parser(object):
    def __init__(self, node):
        self.node = node 
        self.id = int(fieldval(node, 'id'))

    def record_identity(self):
        """ get identity for the failed record """
        for k in ['name', 'full_name', 'id']:
            val = fieldval(self.node, k)
            if val:
                return '{}={}'.format(k, val)

    def get_data(self):
        n = self.node 
        company_name = fieldval(n, 'name')        
        full_name = fieldval(n, 'full_name')

        if not company_name or not full_name: 
            return

        name_parts = full_name.split(' ')
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:])        

        return {
            'name': company_name, 
            'old_id': fieldval(n, 'id'), 
            'url': fieldval(n, 'url'), 
            'users': [{
                'first_name': first_name, 
                'last_name': last_name, 
                'email': fieldval(n, 'email')
            }]
        }


def run(client, reader, limit=None):
    # read all existing, don't send a request if data is already there 
    
    total = 1
    failed = 0
    existing = client.get_existing_ids()
    for node in reader.read():
        parser = Parser(node)
        if parser.id in existing:
            continue 

        data = parser.get_data()

        if data:
            client.save(data)
            #print 'successfull for: {}'.format(data['name'])
        else:
            print 'failed, data problem for: {}'.format(parser.record_identity())
            failed +=1
        total +=1

        if limit and total > limit: 
            print 'reached the limit'
            break
        if total % 10 == 0:
            print 'processing record %s' % total  

    print 'parsed: {} records, {} are failed'.format(total, failed)


# TODO: 
# users are listed under the same name of the company 
# must be treated as users for the same company 
# example : Medtronic

if __name__ == '__main__':
    url = 'http://docker:8008'
    key_secret = 'AKDH6G1O7/x5zmubeuovdnb'
    file_name = 'Companies_ALL_email and full name.xml'

    client = EmpClient(url, key_secret)
    
    reader = XmlReader(file_name)

    run(client, reader)


# TODO: delete example    