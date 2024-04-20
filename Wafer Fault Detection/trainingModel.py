"""
This module is the entry Point for Training the Machine Learning Model

Written By: Saurva Raj Paudel
Version: 1.0
Revisions: None

"""

# Imports
from application_logging import logger
from data_ingestion import data_loader
from data_preprocessing import preprocessing
from data_preprocessing import clustering




class trainModel():
    
    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open("Training_Logs/ModelTrainingLog.txt", 'a+')


    def trainingModel(self):
        self.log_writer.log(self.file_object, "Start of training")

        try:
            #Getting the data from the source
            data_getter = data_loader.Data_Getter(self.file_object, self.log_writer)
            data = data_getter.get_data()

            """doing the data preprocessing"""

            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
        except Exception as e:
            raise Exception()