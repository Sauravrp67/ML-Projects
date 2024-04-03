from datetime import datatime
from Training_Raw_data_validation.rawValidation import Raw_data_validation
from DataTypeValidaton_Insertion_Training.DataTypeValidation import dBOperation
from DataTransfrom_Training.DataTransformation import dataTransform
from application_logging import logger

class train_validation:
    def __init__(self,path):
        self.raw_data = Raw_data_validation(path)
        self.dataTransform = dataTransform()
        self.dBOperation = dBOperation()
        self.file_object = open("Training_Logs/Training_Main_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()


    def train_validation(self):
        try:
            self.log_writer.log(self.file_object, "Start of Validation on files!!")
            #extracting values from predictin shcema
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = self.raw_data.valuesFromSchema()
            #getting the regex defined to validate filename
            regex = self.raw_data.manualRegexCreation()
            # validating filename of prediction files
            self.raw_data.validationFileNameRaw(regex=regex,LengthOfDataStampInFile=LengthOfDateStampInFile,LengthOfTimeStampInFile=LengthOfTimeStampInFile)
            # validating column length in the file
            self.raw_data.validateColumnLength(noofcolumns)
            # validate if any column has all values missing
            self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object, "Raw Data validation Complete!!")

            self.log_writer.log(self.file_object, "Starting Data Transformation!!")

            #replacing blanks in the csv file with "Null" values to insert in table
            self.dataTransform.replaceMissingWithNull()

            self.log_writer.log(self.file_object, "DataTransformation Completed!!")

            self.log_writer.log(self.file_object, "Creating Training_Database and tables on the basis of given schema!!!")
            # create database with given name, if present open the connection! Create table with columns given in schema
            self.dBOperation.createTableDb("Training")
            self.log_writer.log(self.file_object, "Table Creation Completed!!!")
            self.log_writer.log(self.file_object, "Insertion of GoodData into Table of the database sarted!!!")

            self.dBOperation.insertIntoTableGoodData('Training')
            self.log_writer.log(self.file_object,"Insertion in Table Completed")
            self.log_writer.log(self.file_object, "Moving bad files to archive and deleting Bad_Data Folder!!!")
            # Move bad files to archive folder
            self.raw_data.moveBadFilesToArchiveBad()
            self.log_writer.log(self.file_object, "Bad filed moved to Archieve!! Bad folder deleted")
            self.log_writer.log(self.file_object, "Deleting Good data folder")

            # Delete the Good data folder after moving the good data into table
            self.raw_data.deleteExistingGoodDataTrainingFolder()
            self.log_writer.log(self.file_object, "Good Data folder deleted")
            # export data in table to csvfile
            self.dBOperation.selectingDatafromtableintocsv('Training')
            self.file_object.close()

        except Exception as e:
            raise e
            
        
    