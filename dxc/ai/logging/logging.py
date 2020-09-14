import logging


def pipeline_log(pipe):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('pipeline.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info(pipe)
    
def microservice_design_log(microservice_design):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('microservice_design_log.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info(microservice_design)
    
def experiment_design_log(design):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('experiment_design.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info(design)