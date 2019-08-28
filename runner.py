import logging
import logging.config

import sys 
import argparse
import yaml

from utils import get_config

configDict = yaml.load(open('logging-config.yml', 'r'), Loader=yaml.FullLoader)
logging.config.dictConfig(configDict)

import_logger = logging.getLogger('import_log')
export_logger = logging.getLogger('export_log')
logger  = logging.getLogger('console')



if __name__ == '__main__':
    config = get_config()

    ap = argparse.ArgumentParser(description='Data import and export utilities for Careerleaf instance')
    ap.add_argument('command',action="store")

    results = ap.parse_args()  

    if results.command == 'employers-import-xml':
    	from employers import importer
    	importer.run(config)
    if results.command == 'employers-import-csv':
    	from employers import importer_csv
    	importer_csv.run(config)
    elif results.command == 'employers-export':
    	from employers import exporter
    	exporter.run(config)
    elif results.command == 'jobseekers-export':
    	from jobseekers_export import exporter
    	exporter.run(config)    	
    else:
        sys.stderr.write('ERROR: unsupported command: %s\n' % results.command)    	
        ap.print_usage()

