# -*- coding: utf-8 -*-
"""
=============================================================================
Created on: 04-08-2021 07:06 PM
Created by: Digiotai
=============================================================================
Project Name: HousePricePrediction
File Name: logger.py
Description: This file is used for logging different activities
Version: 1.0
Revision: None
=============================================================================
"""
from datetime import datetime


class Logger:
    def __init__(self):
        pass

    def log(self, file_object, log_message):
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")
        file_object.write(
            str(self.date) + "/" + str(self.current_time) + "\t\t" + log_message +"\n")
