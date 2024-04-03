"""
This module is the entry Point for Training the Machine Learning Model

Written By: Saurva Raj Paudel
Version: 1.0
Revisions: None

"""

# Imports
from application_logging import logger
from data_ingestion import data_loader



class trainModel():
    
    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open("Training_Logs/ModelTrainingLog.txt", 'a+')


    def trainingModel(self):
        pass