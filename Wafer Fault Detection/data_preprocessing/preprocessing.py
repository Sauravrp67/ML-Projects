import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer


# What does this class require?
# We need to impute the missing value.
# We need to separate the data with labels
# We need to remove the columns that we don't need, such as the id, wafer shits and all
# And check the columns with zero standard deviation.



class Preprocessor:
    """
    ClassName: Preprocessor
    
    This class shall be used to clean and transform the data before training

    Written By: Saurav Raj Paudel
    Version: 1.0
    Revisions: None

    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def remove_columns(self,data,columns):
        """
            Method Name: remove_columns
            Description: This method removes the given columns from a pandas dataframe.
            Output: A pandas DataFrame after removing the specified columns.
            On Failure: Raise Exception

            Written By: Saurav Raj Paudel
            Version: 1.0
            Revisions: None
        """
        self.logger_object.log(self.file_object, "Entered the remove_columns method of the preprocessor class")
        self.data = data
        self.columns = columns

        try:
            # Drop the column specified in the function parameters
            self.useful_data = self.data.drop(labels=self.columns, axis = 1)
            self.logger_object.log(self.file_object, "Column removal Sucessful. Exited the remove_columns method of the Preprocessor class")
            return self.useful_data
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occured in remove_columns method of the Preprocessor class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Column removal Unsuccessful. Exited the remove_columns method of the Preprocessor class')
            raise Exception()
        
    def seperate_label_feature(self, data,label_column_name):
        """
                Method Name: separate_label_feature
                Description: This method separates the features and a label columns
                Output: Returns two separate Dataframes, one containing features and the other containing Labels.
                On failure: Raise Exception

                Written By: Saurav Raj Paudel
                Version: 1.0
                Revisions : None
        """
        self.logger_object.log(self.file_object, 'Entered the separate_label_feature method of the Preprocessor class')
        try:
            self.X = data.drop(labels = label_column_name, axis = 1)
            self.y = data[label_column_name]
            self.logger_object.log(self.file_object, 'Label Seperation Successful. Exited the separate_label_feature method of the Preprocessor class')
            return self.X, self.y
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occured in separate_label_feature method of the Preprocessor class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')
            raise Exception()
        
    def is_null_present(self,data):
        """
                Method Name: is_null_present
                Description: This method checks whether there are null values present in the pandas Dataframe or not.
                Output: Returns a Boolean Value. True if null values are present in the Dataframe, False if they are not present.
                On Failure : Raise Exception

                Written By: Saurav Raj Paudel
                Version: 1.0
                Revisions: None

        """
        self.logger_object.log(self.file_object, 'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False

        try:
            # Gives out a pandas.Series Object
            self.null_counts = data.isna().sum()
            for i in self.null_counts:
                if i>0:
                    self.null_present = True
                    break
            # We check if any column contains any null values

            if (self.null_present):  
                df_with_null = pd.DataFrame()
                df_with_null['column'] = data.columns
                df_with_null['missing values count'] = np.asarray(data.isna().sum())
                df_with_null.to_csv('preprocessing_data/null_values.csv') # storing the null column information to file
            self.logger_object.log(self.file_object,'FInding missing values is a success. Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            return self.null_present
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occured in is_null_present method of the Preprocessor class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Finding missing value failed. Exited the is_null_present method of the Preprocessor class')
            raise Exception()
        
    def impute_missing_values(self,data):
            """
                Method Name: impute_missing_values

                Description: This method replaces all the missing values in the Dataframe using KNN imputer
                Output: A Dataframe which has all the missing values imputed.   
                On failure: Raises Exception

                Written By: iNeuron Intelligence
                VersionL 1.0
                Revisions:None

            """
            self.logger_object.log(self.file_object, "Entered the impute_missing_values method of the preprocessor class")
            self.data = data
            try:
                imputer = KNNImputer(n_neighbors=3, weights = 'uniform',missing_values = np.nan)
                self.new_array = imputer.fit_transform(self.data)#Impute the missing values
                # Convert the nd-array returned in the step above to a DataFrame
                self.new_data = pd.DataFrame(data=self.new_array,columns = self.data.columns)
                self.logger_object.log(self.file_object, 'Imputing missing values Successful. Exited the impute_missing_values method of the preprocessor class')
                return self.new_data
            except Exception as e:
                self.logger_object.log(self.file_object, 'Exception occured in impute_missing_values method of the Preprocessor class. Exception message: ' + str(e))
                self.logger_object.log(self.file_object,'Imputing missing valued failed.Exited the impute_missing_values method of the Preprocessor class')
                raise Exception()
            
    def get_columns_with_zero_std_deviation(self,data):
        """
                    Method Name: get_columns_with_zero_std_deviation
                    Description: This method finds out the columns which have a standard deviation of zero.
                    Output: List of the columns with standard deviation of zero
                    On Failure: Raise Exception
        """
        self.logger_object.log(self.file_object, "Entered get_columns_with_zero_std_deviation method of the preprocessor class")
        self.columns = data.columns
        self.data_n = data.describe()
        self.col_to_drop = []

        try:
            for x in self.columns:
                if (self.data_n[x]['std'] == 0):
                    self.col_to_drop.append(x)
                self.logger_object.log(self.file_object, "Column search for Standard Deviation of Zero Sucessful. Exiting the method")
                return self.col_to_drop
        except Exception as e:
            self.logger_object.log(self.file_object, "Exception occured in get_columns_with_zero_std_deviation method of the Preprocessor class. Exception message: "+ str(e))
            self.logger_object.log(self.file_object, 'Column search for Standard Deviation of Zero Failed. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            


    