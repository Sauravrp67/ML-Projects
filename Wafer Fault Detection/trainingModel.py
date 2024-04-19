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
        # Logging the start of the training
        self.log_writer.log(self.file_object, "Start of training")

        try:
            #Getting the data from the source
            data_getter = data_loader.Data_Getter(self.file_object, self.log_writer)
            data = data_getter.get_data()

            """doing the data preprocessing"""

            preprocessor=preprocessing.Preprocessor(self.file_object,self.log_writer)
            data=preprocessor.remove_columns(data,['Wafer']) # remove the unnamed column as it doesn't contribute to prediction.

            X,Y=preprocessor.separate_label_feature(data,label_column_name='Output')

            # check if missing values are present in the dataset
            is_null_present=preprocessor.is_null_present(X)

            # if missing values are there, replace them appropriately.
            if(is_null_present):
                X=preprocessor.impute_missing_values(X) # missing value imputation

            cols_to_drop=preprocessor.get_columns_with_zero_std_deviation(X)

            X=preprocessor.remove_columns(X,cols_to_drop)



        except Exception as e:
            raise Exception()