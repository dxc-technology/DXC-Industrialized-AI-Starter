import logging

def experiment_design_log(design):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('experiment_design.log')
    file_handler.setFormatter(formatter)
    if logger.hasHandlers():
        pass
    else:
        logger.addHandler(file_handler)
    logger.info(design)