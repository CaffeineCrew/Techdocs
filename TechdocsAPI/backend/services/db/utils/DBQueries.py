# fix ObjectId & FastApi conflict
import pydantic
from bson.objectid import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

from typing import Union, Tuple, List

from backend.utils import DBConnection
from backend.core.Exceptions import *


class DBQueries:
    @classmethod
    def insert_to_database(cls, table_name:str, data:Union[Tuple, List[Tuple]], cols:List[str]=None):
        con = DBConnection.get_client()
        cursor = con.cursor()
        QUERY = ('INSERT INTO {table_name} '
                 f'({",".join(cols)}) '
                 'VALUES '
                 ).format(table_name=table_name)
        print(data)
        if isinstance(data, list):
            QUERY+="("+",".join(["%s" for _ in range(len(data[0]))])+")"
            cursor.executemany(QUERY, data)
        else:
            QUERY+="("+",".join(["%s" for _ in range(len(data))])+")"
            cursor.execute(QUERY, data)
        con.commit()
        
    @classmethod
    def fetch_data_from_database(cls,table_name:str,cols_to_fetch:Union[str, List[str]], where_clause:str=None):
        con = DBConnection.get_client()
        cursor = con.cursor()
        if isinstance(cols_to_fetch, str):
            cols_to_fetch = [cols_to_fetch]
        cols_to_fetch = ", ".join(cols_to_fetch)
        QUERY = ('SELECT {cols} FROM {table_name}').format(cols=cols_to_fetch, table_name=table_name)
        if where_clause:
            QUERY = QUERY + " WHERE " + where_clause
        cursor.execute(QUERY)
        return cursor.fetchall()
    
    @classmethod
    def update_data_in_database(cls, table_name:str, cols_to_update:Union[str, List[str]], where_clause:str=None, new_values:Union[str, List[str]]=None):
        con = DBConnection.get_client()
        cursor = con.cursor()
        if isinstance(cols_to_update, str):
            cols_to_update = cols_to_update + "=%s"
        else:
            cols_to_update = "=%s, ".join(cols_to_update)
        
        if isinstance(new_values, str):
            new_values = [new_values]
            
        QUERY = ('UPDATE {table_name} SET {cols}').format(table_name=table_name, cols=cols_to_update)
        if where_clause:
            QUERY = QUERY + " WHERE " + where_clause
        cursor.execute(QUERY, new_values)
        con.commit()
        return True
    
    
    
    

        
