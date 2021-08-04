# -*- coding: utf-8 -*-
"""
=============================================================================
Created on: 04-08-2021 06:49 PM
Created by: Digiotai
=============================================================================
Project Name: HousePricePrediction
File Name: database.py
Description: This file consists of database related operations
Version: 1.0
Revision: None
=============================================================================
"""

# importing libraries
import sqlite3
import pandas as pd
from io import StringIO
from .logger import Logger


class SQLiteDB:
    def __init__(self):
        self.fileobject = open("Logs.txt", 'a+')
        self.logger = Logger()

    def table_creation(self, request):
        """
        Method Name: table_creation
        Description: This method is used to create a new table in database .
        Output:  Returns html table created from input data.
        On Failure: None

        Written By: Digiotai
        Version: 1.0
        Revisions: None
        """

        try:
            with sqlite3.connect("db.sqlite3") as c:
                # Getting the uploaded file
                name = request.FILES["input-b6b[]"]
                file = name.read().decode('utf-8')
                data = StringIO(file)
                df = pd.read_csv(data)
                # Storing the input data in database
                df.to_sql('House_pricing', c, if_exists='replace')
                # Logging success message
                self.logger.log(file_object=self.fileobject, log_message="Table Created successfully")
                c.commit()
            return df.to_html(classes='input_table')
        except Exception as e:
            self.logger.log(file_object=self.fileobject, log_message=e)

    def tabledeletion(self):
        """
                Method Name: tabledeletion
                Description: This method is used to delete an existing table from database .
                Output:  None
                On Failure: None

                Written By: Digiotai
                Version: 1.0
                Revisions: None
        """

        try:
            #  connecting to SQlite database
            with sqlite3.connect("db.sqlite3") as c:
                cur = c.cursor()
                cur.execute('DROP TABLE House_pricing')
                cur.execute('DROP TABLE predicted_House_pricing')
                self.logger.log(file_object=self.fileobject, log_message="Table has been deleted successfully")
                c.commit()
        except Exception as e:
            self.logger.log(file_object=self.fileobject, log_message=e)
