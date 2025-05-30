import pandas as pd

class SQLRepository:
    def __init__(self,connection):
        self.connection = connection
        pass

    def insert_table(self, table_name, records, if_exists):
    
        """Insert DataFrame into SQLite database as table

        Parameters
        ----------
        table_name : str
        records : pd.DataFrame
        if_exists : str, optional
            How to behave if the table already exists.

            - 'fail': Raise a ValueError.
            - 'replace': Drop the table before inserting new values.
            - 'append': Insert new values to the existing table.

            Dafault: 'fail'

        Returns
        -------
        dict
            Dictionary has two keys:

            - 'transaction_successful', followed by bool
            - 'records_inserted', followed by int
        """
        n_inserted = records.to_sql(
            name = table_name, con=self.connection, if_exists=if_exists,index=False)
        
        return{
            "transations_successful":True,
            "records_inserted":n_inserted
        }

    def read_table(self, table_name,limit=None):
    
        """Read table from database.

        Parameters
        ----------
        table_name : str
            Name of table in SQLite database.
        limit : int, None, optional
            Number of most recent records to retrieve. If `None`, all
            records are retrieved. By default, `None`.

        Returns
        -------
        pd.DataFrame
            Index is DatetimeIndex "date". Columns are 'open', 'high',
            'low', 'close', and 'volume'. All columns are numeric.
        """
        # Create SQL query (with optional limit)
        if limit:
            sql = f"SELECT * FROM '{table_name}' LIMIT {limit}"
        else:
            sql = f"SELECT * FROM '{table_name}'"

        # Retrieve data, read into DataFrame
        df = pd.read_sql(
            sql=sql, con=self.connection,parse_dates=["Date"],index_col="Date")
        # Return DataFrame
        return df