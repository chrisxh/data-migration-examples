import logging 
import requests
import json

logger  = logging.getLogger('console')


def get_config():
    from ConfigParser import SafeConfigParser
    config = SafeConfigParser()
    config.read('config.ini')
    return config



def get_auth_key(config):
    return '{}/{}'.format(config.get('careerleaf', 'api_key'), config.get('careerleaf', 'api_secret'))


def read_all_pages(url, headers=None):
    while True:
        logger.debug('read_all_pages: %s' % url)
        r = requests.get(url, headers=headers)

        try: 
            resp = json.loads(r.content)
        except:
            logger.error(u'cannot parse: {}'.format(r.content))
            raise 

        yield resp['results']
        url = resp.get('next')
        if not url:
            break
