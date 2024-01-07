import pydantic
from bson.objectid import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str
from typing import Union, Tuple, List
from backend.utils import DBConnection
from backend.core.Exceptions import *

class DBQueries:

    @classmethod
    def insert_to_database(cls, table_name: str, data: Union[Tuple, List[Tuple]], cols: List[str]=None):
        """Wrapper method to insert data to the database.

    Args:
        table_name (str): Name of the table in the database.
        data (Union[Tuple, List[Tuple]]): Data to be inserted in the table. It can be a single tuple or a list of tuples.
        cols (List[str], optional): List of columns in the table. If not provided, all columns will be used.

    Raises:
        ValidationError: If data is not a tuple or a list of tuples.
        InternalServerError: If an error occurs while inserting data to the database.
"""
        con = DBConnection.get_client()
        cursor = con.cursor()
        QUERY = f"INSERT INTO {{table_name}} ({','.join(cols)}) VALUES ".format(table_name=table_name)
        if isinstance(data, list):
            QUERY += '(' + ','.join(['%s' for _ in range(len(data[0]))]) + ')'
            cursor.executemany(QUERY, data)
        else:
            QUERY += '(' + ','.join(['%s' for _ in range(len(data))]) + ')'
            cursor.execute(QUERY, data)
        con.commit()

    @classmethod
    def fetch_data_from_database(cls, table_name: str, cols_to_fetch: Union[str, List[str]], where_clause: str=None):
        """Method to fetch data from database using a SQL query.

    Args:
        table_name: str. Name of the table to fetch data from.
        cols_to_fetch: Union[str, List[str]]. Columns to fetch from the table.
        where_clause: str. Optional. Where clause to filter the data.

    Returns:
        List. List of tuples containing the fetched data.
"""
        con = DBConnection.get_client()
        cursor = con.cursor()
        if isinstance(cols_to_fetch, str):
            cols_to_fetch = [cols_to_fetch]
        cols_to_fetch = ', '.join(cols_to_fetch)
        QUERY = 'SELECT {cols} FROM {table_name}'.format(cols=cols_to_fetch, table_name=table_name)
        if where_clause:
            QUERY = QUERY + ' WHERE ' + where_clause
        cursor.execute(QUERY)
        return cursor.fetchall()

    @classmethod
    def update_data_in_database(cls, table_name: str, cols_to_update: Union[str, List[str]], where_clause: str=None, new_values: Union[str, List[str]]=None):
        """Updates the values of the columns in the table defined by `table_name`
       where the condition defined by `where_clause` is met.

       Args:
           table_name: str. Name of the table.
           cols_to_update: Union[str, List[str]]. Column/s to be updated. If a
                           single column is to be updated, pass it as a string.
                           If multiple columns are to be updated, pass them as a
                           list of strings.
           where_clause: str. Conditions to be met by the rows to be updated.
                          If no condition is to be imposed, pass it as None.
           new_values: Union[str, List[str]]. New values to be set in the
                        columns. If a single column is to be updated, pass the
                        new value as a string. If multiple columns are to be
                        updated, pass the new values as a list of strings.

       Returns:
           bool. True if update was successful, False otherwise.
"""
        con = DBConnection.get_client()
        cursor = con.cursor()
        if isinstance(cols_to_update, str):
            cols_to_update = cols_to_update + '=%s'
        else:
            cols_to_update = '=%s, '.join(cols_to_update)
        if isinstance(new_values, str):
            new_values = [new_values]
        QUERY = 'UPDATE {table_name} SET {cols}'.format(table_name=table_name, cols=cols_to_update)
        if where_clause:
            QUERY = QUERY + ' WHERE ' + where_clause
        cursor.execute(QUERY, new_values)
        con.commit()
        return True