# logger_config.py
import logging
import sys
import os

class CustomLogger(logging.Logger):
    has_error = False
    
    def error(self, msg, *args, **kwargs):
        # Set has_error to True when an error is logged
        self.has_error = True
        super().error(msg, *args, **kwargs)

    def reset_error_state(self):
        self.has_error = False

# Register the custom logger class
logging.setLoggerClass(CustomLogger)

def loglevel() -> str:
    return os.environ.get('LOG_LEVEL', 'INFO') # DEBUG, INFO, WARNING
def debug_mode() -> bool:
    return True if loglevel() == 'DEBUG' else False

def setup_logging(name, level = loglevel()):
    logging.basicConfig(stream=sys.stdout,level=level,
                        format=f'%(levelname)-7s{name.split("/")[-1]} >>> %(message)s',
                        datefmt='%H:%M:%S')
    return logging.getLogger(__name__)
def getLogger():
    return logging.getLogger(__name__)



#import logging
#
#
#class CustomLogger(logging.Logger):
#    has_error = False
#    
#    def error(self, msg, *args, **kwargs):
#        # Set has_error to True when an error is logged
#        self.has_error = True
#        super().error(msg, *args, **kwargs)
#
#    def reset_error_state(self):
#        self.has_error = False
## Register the custom logger class
#logging.setLoggerClass(CustomLogger)
#log = logging.getLogger(__name__)
#
#
#if __name__ == '__main__':
#    import os
#    import sys
#    loglevel = os.environ.get('LOG_LEVEL', 'INFO') # DEBUG, INFO, WARNING
#    DEBUG_MODE = True if loglevel == 'DEBUG' else False
#    logLEVEL = getattr(logging, loglevel)
#    logging.basicConfig(stream=sys.stdout,level=logLEVEL,
#                        format='[basicCONFIG] %(levelname)s - %(message)s',
#                        datefmt='%H:%M:%S')
#
#    print(f"Has error: {log.has_error}")
#    import mytest
#    mytest.func()
#    print(f"Has error: {log.has_error}")
#    log.error("This is an error message.")
#    print(f"Has error: {log.has_error}")
