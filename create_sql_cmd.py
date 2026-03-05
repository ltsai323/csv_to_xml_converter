#!/usr/bin/env python3
import logging
import sys
from pprint import pformat

log = logging.getLogger(__name__)

SQL_SEARCH = '''
SELECT module_name FROM public.module_info
WHERE geometry IS NULL
ORDER BY module_no ASC
'''



if __name__ == '__main__':
    import os
    loglevel = os.environ.get('LOG_LEVEL', 'INFO') # DEBUG, INFO, WARNING
    DEBUG_MODE = True if loglevel == 'DEBUG' else False
    logLEVEL = getattr(logging, loglevel)
    logging.basicConfig(stream=sys.stdout,level=logLEVEL,
                        format=f'%(levelname)-7s%(filename)s#%(lineno)s %(funcName)s() >>> %(message)s',
                        datefmt='%H:%M:%S')


