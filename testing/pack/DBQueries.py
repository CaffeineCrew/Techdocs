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
    This method is used to insert data into a specified table in the database.

    Args:
    table_name (str): The name of the table into which data will be inserted.
    data (Union[Tuple, List[Tuple]]): The data to be inserted into the table. This can be a tuple or a list of tuples, where each tuple represents a row of data.
    cols (List[str], optional): A list of column names in the table. If not provided, the method will assume that all columns are included. Defaults to None.

    Raises:
    None

    Returns:
    None

    """
        '\n    This method is used to insert data into a specified table in the database.\n\n    Args:\n    table_name (str): The name of the table into which data will be inserted.\n    data (Union[Tuple, List[Tuple]]): The data to be inserted into the table. This can be a tuple or a list of tuples, where each tuple represents a row of data.\n    cols (List[str], optional): A list of column names in the table. If not provided, the method will assume that all columns are included. Defaults to None.\n\n    Raises:\n    None\n\n    Returns:\n    None\n\n    '
        '\n    This method is used to insert data into a specified table in the database.\n\n    Args:\n    table_name (str): The name of the table into which data will be inserted.\n    data (Union[Tuple, List[Tuple]]): The data to be inserted into the table. This can be a tuple or a list of tuples, where each tuple represents a row of data.\n    cols (List[str], optional): A list of column names in the table. If not provided, the method will assume that all columns are included. Defaults to None.\n\n    Raises:\n    None\n\n    Returns:\n    None\n\n    '
        '\n    This method is used to insert data into a specified table in the database.\n\n    Args:\n    table_name (str): The name of the table into which data will be inserted.\n    data (Union[Tuple, List[Tuple]]): The data to be inserted into the table. This can be a tuple or a list of tuples, where each tuple represents a row of data.\n    cols (List[str], optional): A list of column names in the table. If not provided, the method will assume that all columns are included. Defaults to None.\n\n    Raises:\n    None\n\n    Returns:\n    None\n\n    '
        '\n    This method is used to insert data into a specified table in the database.\n\n    Args:\n    table_name (str): The name of the table into which data will be inserted.\n    data (Union[Tuple, List[Tuple]]): The data to be inserted into the table. This can be a tuple or a list of tuples, where each tuple represents a row of data.\n    cols (List[str], optional): A list of column names in the table. If not provided, the method will assume that all columns are included. Defaults to None.\n\n    Raises:\n    None\n\n    Returns:\n    None\n\n    '
        '\n    This method is used to insert data into a specified table in the database.\n\n    Args:\n    table_name (str): The name of the table into which data will be inserted.\n    data (Union[Tuple, List[Tuple]]): The data to be inserted into the table. This can be a tuple or a list of tuples, where each tuple represents a row of data.\n    cols (List[str], optional): A list of column names in the table. If not provided, the method will assume that all columns are included. Defaults to None.\n\n    Raises:\n    None\n\n    Returns:\n    None\n\n    '
        '\n    This method is used to insert data into a specified table in the database.\n\n    Args:\n    table_name (str): The name of the table into which data will be inserted.\n    data (Union[Tuple, List[Tuple]]): The data to be inserted into the table. This can be a tuple or a list of tuples, where each tuple represents a row of data.\n    cols (List[str], optional): A list of column names in the table. If not provided, the method will assume that all columns are included. Defaults to None.\n\n    Raises:\n    None\n\n    Returns:\n    None\n\n    '
        '\n        This method is used to insert data into a specified table in the database.\n\n        Args:\n        table_name (str): The name of the table into which data will be inserted.\n        data (Union[Tuple, List[Tuple]]): The data to be inserted into the table. This can be a tuple or a list of tuples, where each tuple represents a row of data.\n        cols (List[str], optional): A list of column names in the table. If not provided, the method will assume that all columns are included. Defaults to None.\n\n        Raises:\n        None\n\n        Returns:\n        None\n\n        '
        '\n    This method is used to insert data into a specified table in the database.\n\n    Args:\n    table_name (str): The name of the table into which data will be inserted.\n    data (Union[Tuple, List[Tuple]]): The data to be inserted into the table. This can be a tuple or a list of tuples, where each tuple represents a row of data.\n    cols (List[str], optional): A list of column names in the table. If not provided, the method will assume that all columns are included. Defaults to None.\n\n    Raises:\n    None\n\n    Returns:\n    None\n\n    '
        '\n    This method is used to insert data into a specified table in the database.\n\n    Args:\n    table_name (str): The name of the table into which data will be inserted.\n    data (Union[Tuple, List[Tuple]]): The data to be inserted into the table. This can be a tuple or a list of tuples, where each tuple represents a row of data.\n    cols (List[str], optional): A list of column names in the table. If not provided, the method will assume that all columns are included. Defaults to None.\n\n    Raises:\n    None\n\n    Returns:\n    None\n    '
        '\n    This method is used to insert data into a specified table in the database.\n\n    Args:\n    table_name (str): The name of the table into which data will be inserted.\n    data (Union[Tuple, List[Tuple]]): The data to be inserted into the table. This can be a tuple or a list of tuples.\n    cols (List[str], optional): A list of column names in the table. If not provided, the method will assume that all columns are included. Defaults to None.\n\n    Raises:\n    None\n\n    Returns:\n    None\n    '
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
    This method is a class method that fetches data from a specified table in the database based on the provided column names and,
    optionally, a WHERE clause.

    Args:
    - table_name: A string representing the name of the table from which to fetch data.
    - cols_to_fetch: A string or a list of strings representing the column(s) to fetch from the table. If a single string,
    it will be treated as a comma-separated list of column names.
    - where_clause: An optional string representing a WHERE clause to filter the fetched data. Defaults to None.

    Returns:
    - cursor.fetchall(): A list of tuples representing the fetched data. Each tuple corresponds to a row in the result set,
    and contains the values of the fetched columns in the order specified.

    Raises:
    - No exceptions are explicitly raised by this method. However, underlying database operations may raise exceptions, which
    are not handled or propagated by this method. It is the responsibility of the caller to handle any exceptions that may occur.

"""
        '\n    This method is a class method that fetches data from a specified table in the database based on the provided column names and,\n    optionally, a WHERE clause.\n\n    Args:\n    - table_name: A string representing the name of the table from which to fetch data.\n    - cols_to_fetch: A string or a list of strings representing the column(s) to fetch from the table. If a single string,\n    it will be treated as a comma-separated list of column names.\n    - where_clause: An optional string representing a WHERE clause to filter the fetched data. Defaults to None.\n\n    Returns:\n    - cursor.fetchall(): A list of tuples representing the fetched data. Each tuple corresponds to a row in the result set,\n    and contains the values of the fetched columns in the order specified.\n\n    Raises:\n    - No exceptions are explicitly raised by this method. However, underlying database operations may raise exceptions, which\n    are not handled or propagated by this method. It is the responsibility of the caller to handle any exceptions that may occur.\n\n    '
        '\n    This method is a class method that fetches data from a specified table in the database based on the provided column names and,\n    optionally, a WHERE clause.\n\n    Args:\n    - table_name: A string representing the name of the table from which to fetch data.\n    - cols_to_fetch: A string or a list of strings representing the column(s) to fetch from the table. If a single string,\n    it will be treated as a comma-separated list of column names.\n    - where_clause: An optional string representing a WHERE clause to filter the fetched data. Defaults to None.\n\n    Returns:\n    - cursor.fetchall(): A list of tuples representing the fetched data. Each tuple corresponds to a row in the result set,\n    and contains the values of the fetched columns in the order specified.\n\n    Raises:\n    - No exceptions are explicitly raised by this method. However, underlying database operations may raise exceptions, which\n    are not handled or propagated by this method. It is the responsibility of the caller to handle any exceptions that may occur.\n\n    '
        '\n    This method is a class method that fetches data from a specified table in the database based on the provided column names and,\n    optionally, a WHERE clause.\n\n    Args:\n    - table_name: A string representing the name of the table from which to fetch data.\n    - cols_to_fetch: A string or a list of strings representing the column(s) to fetch from the table. If a single string,\n    it will be treated as a comma-separated list of column names.\n    - where_clause: An optional string representing a WHERE clause to filter the fetched data. Defaults to None.\n\n    Returns:\n    - cursor.fetchall(): A list of tuples representing the fetched data. Each tuple corresponds to a row in the result set,\n    and contains the values of the fetched columns in the order specified.\n\n    Raises:\n    - No exceptions are explicitly raised by this method. However, underlying database operations may raise exceptions, which\n    are not handled or propagated by this method. It is the responsibility of the caller to handle any exceptions that may occur.\n\n    '
        '\n    This method is a class method that fetches data from a specified table in the database based on the provided column names and,\n    optionally, a WHERE clause.\n\n    Args:\n    - table_name: A string representing the name of the table from which to fetch data.\n    - cols_to_fetch: A string or a list of strings representing the column(s) to fetch from the table. If a single string,\n    it will be treated as a comma-separated list of column names.\n    - where_clause: An optional string representing a WHERE clause to filter the fetched data. Defaults to None.\n\n    Returns:\n    - cursor.fetchall(): A list of tuples representing the fetched data. Each tuple corresponds to a row in the result set,\n    and contains the values of the fetched columns in the order specified.\n\n    Raises:\n    - No exceptions are explicitly raised by this method. However, underlying database operations may raise exceptions, which\n    are not handled or propagated by this method. It is the responsibility of the caller to handle any exceptions that may occur.\n\n    '
        '\n    This method is a class method that fetches data from a specified table in the database based on the provided column names and,\n    optionally, a WHERE clause.\n\n    Args:\n    - table_name: A string representing the name of the table from which to fetch data.\n    - cols_to_fetch: A string or a list of strings representing the column(s) to fetch from the table. If a single string,\n    it will be treated as a comma-separated list of column names.\n    - where_clause: An optional string representing a WHERE clause to filter the fetched data. Defaults to None.\n\n    Returns:\n    - cursor.fetchall(): A list of tuples representing the fetched data. Each tuple corresponds to a row in the result set,\n    and contains the values of the fetched columns in the order specified.\n\n    Raises:\n    - No exceptions are explicitly raised by this method. However, underlying database operations may raise exceptions, which\n    are not handled or propagated by this method. It is the responsibility of the caller to handle any exceptions that may occur.\n\n    '
        '\n    This method is a class method that fetches data from a specified table in the database based on the provided column names and,\n    optionally, a WHERE clause.\n\n    Args:\n    - table_name: A string representing the name of the table from which to fetch data.\n    - cols_to_fetch: A string or a list of strings representing the column(s) to fetch from the table. If a single string,\n    it will be treated as a comma-separated list of column names.\n    - where_clause: An optional string representing a WHERE clause to filter the fetched data. Defaults to None.\n\n    Returns:\n    - cursor.fetchall(): A list of tuples representing the fetched data. Each tuple corresponds to a row in the result set,\n    and contains the values of the fetched columns in the order specified.\n\n    Raises:\n    - No exceptions are explicitly raised by this method. However, underlying database operations may raise exceptions, which\n    are not handled or propagated by this method. It is the responsibility of the caller to handle any exceptions that may occur.\n\n    '
        '\n    This method is a class method that fetches data from a specified table in the database based on the provided column names and,\n    optionally, a WHERE clause.\n\n    Args:\n    - table_name: A string representing the name of the table from which to fetch data.\n    - cols_to_fetch: A string or a list of strings representing the column(s) to fetch from the table. If a single string,\n    it will be treated as a comma-separated list of column names.\n    - where_clause: An optional string representing a WHERE clause to filter the fetched data. Defaults to None.\n\n    Returns:\n    - cursor.fetchall(): A list of tuples representing the fetched data. Each tuple corresponds to a row in the result set,\n    and contains the values of the fetched columns in the order specified.\n\n    Raises:\n    - No exceptions are explicitly raised by this method. However, underlying database operations may raise exceptions, which\n    are not handled or propagated by this method. It is the responsibility of the caller to handle any exceptions that may occur.\n\n    '
        '\n    This method is a class method that fetches data from a specified table in the database based on the provided column names and,\n    optionally, a WHERE clause.\n\n    Args:\n    - table_name: A string representing the name of the table from which to fetch data.\n    - cols_to_fetch: A string or a list of strings representing the column(s) to fetch from the table. If a single string,\n    it will be treated as a comma-separated list of column names.\n    - where_clause: An optional string representing a WHERE clause to filter the fetched data. Defaults to None.\n\n    Returns:\n    - cursor.fetchall(): A list of tuples representing the fetched data. Each tuple corresponds to a row in the result set,\n    and contains the values of the fetched columns in the order specified.\n\n    Raises:\n    - No exceptions are explicitly raised by this method. However, underlying database operations may raise exceptions, which\n    are not handled or propagated by this method. It is the responsibility of the caller to handle any exceptions that may occur.\n\n    '
        '\n    This method is a class method that fetches data from a specified table in the database based on the provided column names and,\n    optionally, a WHERE clause.\n\n    Args:\n    - table_name: A string representing the name of the table from which to fetch data.\n    - cols_to_fetch: A string or a list of strings representing the column(s) to fetch from the table. If a single string,\n    it will be treated as a comma-separated list of column names.\n    - where_clause: An optional string representing a WHERE clause to filter the fetched data. Defaults to None.\n\n    Returns:\n    - cursor.fetchall(): A list of tuples representing the fetched data. Each tuple corresponds to a row in the result set,\n    and contains the values of the fetched columns in the order specified.\n\n    Raises:\n    - No exceptions are explicitly raised by this method. However, underlying database operations may raise exceptions, which\n    are not handled or propagated by this method. It is the responsibility of the caller to handle any exceptions that may occur.\n    '
        '\n    This method is a class method that fetches data from a specified table in the database based on the provided column names and,\n    optionally, a WHERE clause.\n\n    Args:\n    - table_name: A string representing the name of the table from which to fetch data.\n    - cols_to_fetch: A string or a list of strings representing the column(s) to fetch from the table. If a single string,\n    it will be treated as a comma-separated list of column names.\n    - where_clause: An optional string representing a WHERE clause to filter the fetched data. Defaults to None.\n\n    Returns:\n    - cursor.fetchall(): A list of tuples representing the fetched data. Each tuple corresponds to a row in the result set,\n    and contains the values of the fetched columns in the order specified.\n\n    Raises:\n    - No exceptions are explicitly raised by this method. However, underlying database operations may raise exceptions, which\n    are not handled or propagated by this method. It is the responsibility of the caller to handle any exceptions that may occur.\n    '
        '\n    This method is a class method that fetches data from a specified table in the database based on the provided column names and,\n    optionally, a WHERE clause.\n\n    Args:\n    - table_name: A string representing the name of the table from which to fetch data.\n    - cols_to_fetch: A string or a list of strings representing the column(s) to fetch from the table. If a single string,\n    it will be treated as a comma-separated list of column names.\n    - where_clause: An optional string representing a WHERE clause to filter the fetched data. Defaults to None.\n\n    Returns:\n    - cursor.fetchall(): A list of tuples representing the fetched data. Each tuple corresponds to a row in the result set,\n    and contains the values of the fetched columns in the order specified.\n\n    Raises:\n    - No exceptions are explicitly raised by this method. However, underlying database operations may raise exceptions, which\n    are not handled or propagated by this method. It is the responsibility of the caller to handle any exceptions that may occur.\n    '
        '\n    This method is a class method that fetches data from a specified table in the database based on the provided column names and,\n    optionally, a WHERE clause.\n\n    Args:\n    - table_name: A string representing the name of the table from which to fetch data.\n    - cols_to_fetch: A string or a list of strings representing the column(s) to fetch from the table. If a single string,\n    it will be treated as a comma-separated list of column names.\n    - where_clause: An optional string representing a WHERE clause to filter the fetched data. Defaults to None.\n\n    Returns:\n    - cursor.fetchall(): A list of tuples representing the fetched data. Each tuple corresponds to a row in the result set,\n    and contains the values of the fetched columns in the order specified.\n\n    Raises:\n    - No exceptions are explicitly raised by this method. However, underlying database operations may raise exceptions, which\n    are not handled or propagated by this method. It is the responsibility of the caller to handle any exceptions that may occur.\n    '
        '\n    This method is a class method that fetches data from a specified table in the database based on the provided column names and,\n    optionally, a WHERE clause.\n\n    Args:\n    - table_name: A string representing the name of the table from which to fetch data.\n    - cols_to_fetch: A string or a list of strings representing the column(s) to fetch from the table. If a single string,\n    it will be treated as a comma-separated list of column names.\n    - where_clause: An optional string representing a WHERE clause to filter the fetched data. Defaults to None.\n\n    Returns:\n    - cursor.fetchall(): A list of tuples representing the fetched data. Each tuple corresponds to a row in the result set,\n    and contains the values of the fetched columns in the order specified.\n\n    Raises:\n    - No exceptions are explicitly raised by this method. However, underlying database operations may raise exceptions, which\n    are not handled or propagated by this method. It is the responsibility of the caller to handle any exceptions that may occur.\n    '
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
    This method updates the data in a specified table in the database.

    Args:
        table_name (str): The name of the table in which the data needs to be updated.
        cols_to_update (Union[str, List[str]]): The column(s) to be updated. If a single string, it should end with '=%s'. If a list, it should contain strings, each ending with '=%s'.
        where_clause (str, optional): The WHERE clause of the SQL query. Defaults to None.
        new_values (Union[str, List[str]], optional): The new values to be updated in the columns. If a single string, it should be a list of new values. If a list, it should contain the new values for each column. Defaults to None.

    Returns:
        bool: Returns True if the data is successfully updated in the database.

    Raises:
        Exception: If the database connection fails or the query execution fails.
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