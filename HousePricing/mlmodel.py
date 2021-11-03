# -*- coding: utf-8 -*-
"""
=============================================================================
Created on: 04-08-2021 08:02 PM
Created by: Digiotai
=============================================================================
Project Name: HousePricePrediction
File Name: mlmodel.py
Description:  This file consists of methods used for predicting the input data
Version: 1.0
Revision: None
=============================================================================
"""

# importing libraries
import pandas as pd
import sqlite3
import joblib
from .logger import Logger
import xgboost

class mlmodel:
    def __init__(self):
        self.logger = Logger()
        self.fileobject = open("Logs.txt", 'a+')

    def model_prediction(self):
        """
                Method Name: model_prediction
                Description: This method is used to predict the input data.
                Input: Data from House_pricing table in database
                Output:  Returns html table created from predicted data.
                On Failure: None

                Written By: Digiotai
                Version: 1.0
                Revisions: None
        """
        self.logger.log(file_object=self.fileobject,log_message='ML Model')
        with sqlite3.connect("db.sqlite3") as c:
            try:
                self.logger.log(file_object=self.fileobject,log_message='Fetching input data from database started')
                Y_test_original = pd.read_sql_query('SELECT * from House_pricing', c)
                self.logger.log(file_object=self.fileobject, log_message='Fetching input data from database completed')
                # load
                self.logger.log(file_object=self.fileobject, log_message='Loading pickle file')
                clf2 = joblib.load("housepredction.pkl")

                # To measure how recently the House was re-modified - calculate a column by subtracting YearBuilt from YearRemodAdd.
                # The notes on the data says - YearRemodAdd: Remodel date (same as construction date if no remodeling or additions)

                Y_test_original['years_since_update'] = Y_test_original['YearRemodAdd'] - Y_test_original['YearBuilt']
                Y_test_original['garage_value'] = Y_test_original['YearBuilt'] * Y_test_original['GarageCars']

                Y_test_original = Y_test_original.drop(columns=['GarageCars', 'index'])


                feature_numerical_columns = [col_name for col_name in Y_test_original.columns if
                                             Y_test_original[col_name].dtype in ['int64', 'float64']]

                feature_categorical_cols = [col_name for col_name in Y_test_original.columns if
                                            Y_test_original[col_name].nunique() < 50 and
                                            Y_test_original[col_name].dtype in ['object', 'bool']]
                self.logger.log(file_object=self.fileobject, log_message='Input prediction started')
                prediction = clf2.predict(Y_test_original)
                self.logger.log(file_object=self.fileobject, log_message='Input prediction completed')
                Y_test_original['Predicted Sales Price'] = prediction
                Y_test_original.to_sql('predicted_House_pricing', c, if_exists='replace')
                self.logger.log(file_object=self.fileobject, log_message='Prediction data pushed to database')
                self.fileobject.close()
                return {'download': 'Click here to download the predicted results',
                        'data': Y_test_original.to_html(classes='output_table')}
            except Exception as e:
                return {'data': e}
