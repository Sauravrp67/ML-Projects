import sqlite3
from datetime import datetime
from os import listdir
import os
import re
import json
import shutil
import pandas as pd
from application_logging.logger import App_Logger




class Raw_data_validation:

    """
            This class will be usef for handling all the validation done on the Raw Training Data!!.

            Written By: Saurav Raj Paudel
            Version: 1.0
            Revisions: None

    
    """
    def __init__(self,path):
        self.Batch_Directory = path
        self.schema_path = 'schema_training.json'
        self.logger = App_Logger()


    def valuesFromSchema(self):
        """
                    Method: valuesFromSchema
                    Description: This method extracts all the relevant information from the pre-defined "Schema" file.
                        Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
                        On Failure: Raise ValueError,KeyError,Exception

                    Written By: Saurav Raj Paudel
                    Version: 1.0
                    Revisions: None
        
        """

        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()

            pattern = dic['SampleFileName']
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStamInFile = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            NumberOfColumns = dic['NumberOfColumns']

            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", "a+")
            message = "LengthOfDateStampInFile:: %s" %LengthOfDateStampInFile + "\t" + "LengthOfTimeStamInFile:: %s" %LengthOfTimeStamInFile + "\t" + "NumberofColumns:: %s" %NumberOfColumns
            self.logger.log(file, message)

            file.close()

        except ValueError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", "a+")
            self.logger.log(file, "ValueError:Value not found inside schema_training.json")
            file.close()
            raise ValueError
        
        except KeyError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", "a+")
            self.logger.log(file, "KeyError:Key value error incorrect key passed")
            file.close()
            raise KeyError
        
        except Exception as e:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", "a+")
            self.logger.log(file, str(e))
            file.close()
            raise e
        
        return LengthOfDateStampInFile,LengthOfTimeStamInFile,column_names,NumberOfColumns
    

    def manualRegexCreation(self):

        """
                    Method Name: manualRegexCreation
                    Description: This method contains a manually defined regex based on the "FileName" given in "Schema" file.
                                This Regex is used to validate the filename of the training data.

                    Output: Regex pattern
                    On Failure : None

                    Written By: Saurav Raj Paudel

                    Revisions: None
        """
        regex = "['wafer']+['\_']+[\d_]+[\d_]+\.csv"
        return regex
    
    def createDirectoryForGoodBadRawData(self):
        """
                    Method Name: createDirectoryForGoodBadRawData
                    Description: This method creates directories to store the Good Data and Bad Data
                                after validating the training data.

                    Output: None
                    On Failure : OSError
                    Written By : Saurav Raj Paudel

                    Version: 1.0
                    Revisions: None

        """
        try:
            path = os.path.join("Training_Raw_files_validated/", "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)

            path = os.path.join("Training_Raw_files_validated/", "Bad_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)

        except OSError as ex:
            file = open("Training_Logs/GeneralLog.txt", "a+")
            self.logger.log(file, "Error while creating Directory %s:" % ex)
            file.close()
            raise OSError
        

    def deleteExistingGoodDataTrainingFolder(self):

        """
                                Method Name: deleteExistingGoodDataTrainingFolder
                                Description: This method deletes the directory made to store the Good Data
                                                after loading the data in the table. Once the good files are
                                                loaded in the DB, deleting the directory ensures space optimization.

                                Output: None
                                On Failure: OSError

                                Written By: Saurav Raj Paudel

                                Version: 1.0
                                Revisions: None
        
        """
        try:
            path = 'Training_Raw_files_validated/'

            if os.path.isdir(path + 'Good_Raw/'):
                shutil.rmtree(path + 'Good_Raw/')
                file = open("Training_Logs/GeneralLog.txt", 'a+')
                self.logger.log(file, "GoodRaw Directory deleted sucessfully!!!")
                file.close()

        except OSError as s:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file, "Error while Deleting Directory : %s" %s)
            file.close()
            raise OSError
    def deleteExistingBadDataTrainingFolder(self):

        """
                        Method Name: deletingExistingBadDataTrainingFolder

                        Descroption: This method deletes the directory made to store the bad Data.
                        Output: None
                        On Failure : OSError

                        Written By : Saruav Raj Paudel
                        Version: 1.0
                        Revisions: None
        
        """

        try: 
            path = 'Training_Raw_files_validated/'
            if os.path.isdir(path + 'Bad_Raw'):
                shutil.rmtree(path + 'Bad_Raw')
                file = open('Training_Logs/GeneralLog.txt', 'a+')
                self.logger.log(file,"BadRaw Directory Deleted Sucessfully!!!")
                file.close()
        except OSError:
            file = open('Training_Logs/GeneralLog.txt', 'a+')
            self.logger.log(file, "Error while Deleting Directory : %s" %s)
            file.close()
            raise OSError
        
    def moveBadFilesToArchiveBad(self):
        """
                    Method Name : moveBadFilesToArchiveBad
                    Description: This method deletes the directory made to store the Bad Data after moving the data in an archive folder. We archive the bad
                                    files to send them back to the client for invalid data issues.

                    Output: None
                    On failure: OSError

                    Written By: Saurav Raj Paudel

                    Revision: None
        
        """
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")

        try:
            source = 'Training_Raw_files_validated/Bad_Raw'
            if os.path.isdir(source):
                path = "TrainingArchiveBadData"
                if not os.path.isdir(path):
                    os.makedirs(path)

                dest = 'TrainingArchiveBadData/BadData_' + str(date)+ "_" + str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)

                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source + f, dest)
                file = open("Training_Logs/GeneralLog.txt", 'a+')
                self.logger.log(file, "Bad files moved to archive")
                path = 'Training_Raw_files_validated/'
                if os.path.isdir(path + 'Bad_Raw/'):
                    shutil.rmtree(path + 'Bad_Raw/')
                self.logger.log(file, "Bad Raw Data Folder Deleted Sucessfully!!")
                file.close()

        except Exception as e:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file, "Error while moving bad files to archive:: %s" %e)
            file.close()
            raise e
        
    def validationFileNameRaw(self,regex,LengthOfDataStampInFile, LengthOfTimeStampInFile):
        """
                Method Name: validationFileNameRaw
                Description: This function validates the name of the training csv files as per given name in the schema!
                                 Regex pattern is used to do the validation.If name format do not match the file is moved
                                 to Bad Raw Data folder else in Good raw data.
                Output: None
                On Failure: Exception

                Written By: Saurav Raj Paudel
                Version: 1.0
                Revision: None
        
        
        """
        #pattern = "['Wafer']+['\_'']+[\d_]+[\d]+\.csv"
        # Delete the directories for good and bad data in case last run was unsucessful and folders were not deleted.
        self.deleteExistingBadDataTrainingFolder()
        self.deleteExistingGoodDataTrainingFolder()
        #create new directories
        self.createDirectoryForGoodBadRawData()
        onlyfiles = [f for f in listdir(self.Batch_Directory)]

        # try:
        #     f = open("Training_Logs/nameValidationLog.txt",'a+')
        #     for filename in onlyfiles:
        #         if (re.match(regex, filename)):
        #             splitAtDot = re.split('.csv', filename)

