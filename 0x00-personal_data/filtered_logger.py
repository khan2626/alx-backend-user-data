#!/usr/bin/env python3
"""A script for handling pii"""


from typing import List
import re
import logging
from os import environ
import mysql.connector



PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, 
                 message: str, separator: str) -> str:
    """a function called filter_datum that returns the log message obfuscated:

    Arguments:
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating all 
    fields in the log line (message)
    The function should use a regex to replace occurrences of certain field values.
    filter_datum should be less than 5 lines long and use re.sub to perform the 
    substitution with a single regex.
    """


    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
        """it returns logging.logger object.
        """

        logger = logging.getLogger('user_data')
        logger.setLevel(logging.INFO)
        logger.propagate = False

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
        logger.addHandler(stream_handler)

        return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
     


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    
    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    
    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum
        """

        record.msg = filter_datum(self.fields, self.REDACTION, 
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
    
    
    
        


        


