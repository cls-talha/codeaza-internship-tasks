import pandas as pd
import mysql.connector
from sqlalchemy import create_engine


#read datafram class
class ReadCSV:
    def __init__(self, path, index_col=0):
        self.path = path
        self.index_col = index_col

    def read(self):
        dataframe = pd.read_csv(self.path, index_col=self.index_col)
        return dataframe

# database class to add data in database
class Add_Data:
    def __init__(self, dataframe, user_name: str, password: str, database: str):
        self.dataframe = dataframe
        self.user_name = user_name
        self.password = password
        self.database = database

    def execute_query(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user=self.user_name, # your username
                password=self.password, # your password
                database=self.database # database name
            )

            cursor = mydb.cursor()
            print("[INFO] Database connected: ", mydb.is_connected())

            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            print("[INFO] Inserting data in table", tables[0][0])

            # Create the SQLAlchemy engine
            engine = create_engine(f"mysql+mysqlconnector://{self.user_name}:{self.password}@localhost/{self.database}")

            # Write the DataFrame to MySQL
            self.dataframe.to_sql(name=tables[0][0], con=engine, if_exists='replace', index=True)

            print("[INFO] Data inserted successfully")
            cursor.close()
            mydb.close()

        except mysql.connector.Error as err:
            raise ValueError("Database not connected", str(err))


if __name__ == "__main__":
    quran_data = ReadCSV('/home/talha/Documents/Database and api/quran_data.csv')
    dataframe = quran_data.read()

    sql_query = Add_Data(dataframe, "talha", "izmeh", "mydatabase")
    sql_query.execute_query()
