import logging

import json
import re
import requests 

from csv_utils import fieldval, CsvReader
from utils import read_all_pages, get_auth_key
  
import_logger = logging.getLogger('import_log')
logger  = logging.getLogger('console')



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

        import_logger.debug('Save with headers [{}]'.format(headers))

        if not id:
            url = self.list_url
            import_logger.debug(url)
            res = requests.post(url, data=json.dumps(data), headers=headers)
        else:
            raise NotImplementedError("update is not implemented")

        if res.status_code not in [200, 201]: 
            import_logger.info('failed for record: %s, status_code=%s' % (data['name'], res.status_code))
            import_logger.error('input was:', data)
            import_logger.error('%s', data)
            import_logger.error('response was:')
            import_logger.error(res.content)            
            return False 
        
        #res.raise_for_status()
        #print 'saved: {}'.format(data['name'])
        return True

class Parser(object):
    def __init__(self, node):
        self.node = node 
        self.id = int(fieldval(node, 'id'))
        self.users = node['users']

    def record_identity(self):
        """ get identity for the failed record """
        for k in ['name', 'full_name', 'id']:
            val = fieldval(self.node, k)
            if val:
                return '{}={}'.format(k, val)

    def _fix_url(self, url):
        if url and not re.match(r'http(s)?:', url):
           url = 'http://{}'.format(url) 
        return url

    def get_data(self):
        n = self.node 
        company_name = fieldval(n, 'name')                

        if not company_name: 
            return

        assert self.users, "must have at least one user: %s" % self.id

        return {
            'name': company_name, 
            'old_id': fieldval(n, 'old_id'), 
            'url': self._fix_url(fieldval(n, 'url')), 
            'users': self.users,
            'logo_url': fieldval(n, 'logo_url')
        }



from collections import defaultdict




def run(config, limit=None):
    # read all existing, don't send a request if data is already there 
    url = config.get('careerleaf', 'url')
    key_secret = key_secret =  get_auth_key(config) 
    file_name = config.get('employers-import-csv', 'file')

    client = EmpClient(url, key_secret)
    

    reader = CsvReader(file_name)
    #output = reader.read()
    #print(json.dumps(output, indent=4))

    total = 0
    success_count = 0
    skipped = 0
    existing = client.get_existing_ids()
    processed_ids = []
    for node in reader.read():
        import_logger.debug(node['id'])
        parser = Parser(node)
        id = parser.id

        if id in existing:
            import_logger.debug('skipping : %s' % id)
            skipped +=1
            continue 

        assert not id in processed_ids 
        processed_ids.append(id) # ensuring that we do not process more than once       

        data = parser.get_data()

        is_successful = client.save(data)
        if is_successful:
            success_count+=1
            import_logger.info('successful for: {}'.format(data['name']))
        else:
            import_logger.error('failed, data problem for: {}'.format(parser.record_identity()))

        total +=1

        if limit and total > limit: 
            import_logger.info('reached the limit: {}, stopping'.format(limit) )
            break
        if total % 10 == 0:
            import_logger.info('processing record %s' % total)  

    import_logger.info('parsed {} records, {} are successfull, {} are failed, {} skipped'.format(total, success_count, (total - success_count), skipped))



# TODO: delete example    