import pydantic
from bson.objectid import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str
from typing import Union, Tuple, List
from backend.utils import DBConnection
from backend.core.Exceptions import *

class DBQueries:

    @classmethod
    def insert_to_database(cls, table_name: str, data: Union[Tuple, List[Tuple]], cols: List[str]=None):
        """
    This method is used to insert data into a specific table in the database.

    Args:
        table_name (str): The name of the table into which data will be inserted.
        data (Union[Tuple, List[Tuple]]): The data to be inserted into the table. This can be a tuple or a list of tuples.
                                          Each tuple represents a row of data to be inserted.
        cols (List[str], optional): A list of column names in the table. If not provided, the method will assume that all columns
                                    should be included. Defaults to None.

    Raises:
        Exception: If the database connection fails.

    Returns:
        None
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
        """
    This method fetches data from a specified table in the database based on the provided column names and optional
    WHERE clause.

    Args:
        table_name (str): The name of the table from which to fetch data.
        cols_to_fetch (Union[str, List[str]]): The column(s) to fetch from the table. Can be a single string or a
            list of strings. If a single string, it will be treated as a comma-separated list.
        where_clause (str, optional): An optional WHERE clause to filter the fetched data. Defaults to None.

    Returns:
        List[List[str]]: A list of lists, where each inner list represents a row of fetched data, and each item in
            the inner list corresponds to the value of a fetched column.

    Raises:
        None
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
        """
    This method updates the specified columns in the given table in the database.

    Args:
        table_name (str): The name of the table in which the data needs to be updated.
        cols_to_update (Union[str, List[str]]): The columns to be updated. If provided as a string, it should be a comma-separated list of column names. If provided as a list, it should be a list of column names.
        where_clause (str, optional): The WHERE clause to specify the condition for updating the data. Defaults to None.
        new_values (Union[str, List[str]], optional): The new values to be updated in the columns. If provided as a string, it should be a comma-separated list of new values. If provided as a list, it should be a list of new values. Defaults to None.

    Returns:
        bool: Returns True if the data is successfully updated in the database.

    Raises:
        Exception: If the database connection fails or the query execution fails, an Exception is raised.
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