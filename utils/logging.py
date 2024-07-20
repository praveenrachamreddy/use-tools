import logging

def setup_logging(log_file='agent.log'):
    logging.basicConfig(level=logging.INFO, filename=log_file,
                        format='%(asctime)s:%(levelname)s:%(message)s')

def log_error(error):
    logging.error(error)
