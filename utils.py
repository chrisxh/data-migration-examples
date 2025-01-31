import logging 
import requests
import json
import configparser

logger  = logging.getLogger('import_log')


def get_config():
    from configparser import SafeConfigParser
    config = SafeConfigParser()
    config.read('config.ini')
    return config



def get_auth_key(config):
    return '{}/{}'.format(config.get('careerleaf', 'api_key'), config.get('careerleaf', 'api_secret'))


def read_all_pages(url, headers=None, import_limit=None):
    page=1
    failed_records=0
    
    while True:
        page=page+1
        r = requests.get(url, headers=headers)
        try:
            logger.debug(u'GET {} returned {}'.format(url, r.status_code)) 
            resp = r.json()#json.loads(r.content)
        except:
            logger.error(u'Invalid JSON from: {}'.format(url))
            failed_records=failed_records+1
            url = url.replace("page={}".format(page-1),"page={}".format(page))
            continue

        yield resp['results']
        if import_limit and page > import_limit:
            logger.debug('completed, {} records failed'.format(failed_records))
            break
        url = resp.get('next')
        if not url:
            logger.debug('completed, {} records failed'.format(failed_records))
            break
