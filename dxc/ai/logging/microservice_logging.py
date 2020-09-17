import logging

def microservice_design_log(microservice_design):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('microservice_design_log.log')
    file_handler.setFormatter(formatter)
    if logger.hasHandlers():
        pass
    else:
        logger.addHandler(file_handler)
    logger.info(microservice_design)
