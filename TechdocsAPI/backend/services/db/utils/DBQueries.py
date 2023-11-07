from typing import Union, Tuple, List
from backend.utils import DBConnection
from backend.core.Exceptions import *

class DBQueries:

    @classmethod
    def insert_to_database(cls, table_name: str, data: Union[Tuple, List[Tuple]], cols: List[str]=None):
        """
    This method is used to insert data into a specified table in the database.

    Args:
    table_name (str): The name of the table where the data will be inserted.
    data (Union[Tuple, List[Tuple]]): The data to be inserted into the table. It can be either a tuple or a list of tuples.
    cols (List[str], optional): A list of column names in the table. If not provided, the method will assume that all columns are included. Defaults to None.

    Raises:
    Exception: If there is an error while connecting to the database or executing the query.

    Returns:
    None: This method does not return anything.
    """
        con = DBConnection.get_client()
        cursor = con.cursor()
        QUERY = ('INSERT INTO {table_name} '
                 f'({",".join(cols)}) '
                 'VALUES '
                 ).format(table_name=table_name)
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
    This method fetches data from a specified table in the database based on the specified column(s) and optional WHERE clause.

    Args:
        table_name (str): The name of the table from which to fetch data.
        cols_to_fetch (Union[str, List[str]]): The column(s) to fetch from the table. Can be a single string or a list of strings.
        where_clause (str, optional): An optional WHERE clause to filter the fetched data. Defaults to None.

    Returns:
        List[tuple]: A list of tuples representing the fetched data, where each tuple corresponds to a row and contains the values of the fetched columns in the order specified.

    Raises:
        None
    """
        con = DBConnection.get_client()
        cursor = con.cursor()
        if isinstance(cols_to_fetch, str):
            cols_to_fetch = [cols_to_fetch]
        cols_to_fetch = ', '.join(cols_to_fetch)
        QUERY = ('SELECT {cols} FROM {table_name}').format(cols=cols_to_fetch, table_name=table_name)
        if where_clause:
            QUERY = QUERY + ' WHERE ' + where_clause
        cursor.execute(QUERY)
        return cursor.fetchall()

    @classmethod
    def update_data_in_database(cls, table_name: str, cols_to_update: Union[str, List[str]], where_clause: str=None, new_values: Union[str, List[str]]=None):
        """
    This function is used to update the data in a specific table in the database.

    Args:
    table_name (str): The name of the table where the data needs to be updated.
    cols_to_update (Union[str, List[str]]): The column(s) to be updated. If a string, it should end with '=%s'. If a list, it should contain the column names separated by '=%s, '.join(cols_to_update).
    where_clause (str, optional): The WHERE clause to specify the condition for updating the data. Defaults to None.
    new_values (Union[str, List[str]], optional): The new values to be updated in the columns. If a string, it should be a list [new_value]. If a list, it should contain the new values corresponding to the columns. Defaults to None.

    Returns:
    bool: Returns True if the data is successfully updated in the database.

    Raises:
    None
    """
        con = DBConnection.get_client()
        cursor = con.cursor()
        if isinstance(cols_to_update, str):
            cols_to_update = cols_to_update + '=%s'
        else:
            cols_to_update = '=%s, '.join(cols_to_update)
        if isinstance(new_values, str):
            new_values = [new_values]
        QUERY = ('UPDATE {table_name} SET {cols}').format(table_name=table_name, cols=cols_to_update)
        if where_clause:
            QUERY = QUERY + ' WHERE ' + where_clause
        cursor.execute(QUERY, new_values)
        con.commit()
        return True