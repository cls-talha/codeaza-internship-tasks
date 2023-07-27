import mysql.connector as connector
from sqlalchemy import create_engine
import logging

class Database:
    def __init__(self, username: str, password: str, database: str) -> None:
        self.username = username
        self.password = password
        self.database = database
        try:
            self.my_database = connector.connect(
                host="localhost",
                user=self.username,
                password=self.password,
                database=self.database
            )
            if self.my_database.is_connected():
                logging.info("[INFO] Connected with database")
        
        except connector.Error as e:
            logging.error("[ERROR] Connection Failed")
            raise ValueError(str(e))

    def insert_data(self, dataframe):
        try:
            self.cursor = self.my_database.cursor()
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            logging.info("Tables: %s", tables)
            engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@localhost/{self.database}")
            dataframe.to_sql(name='yahoo_records', con=engine, if_exists='replace', index=True)
            self.my_database.commit()
            logging.info("[INFO] Data inserted successfully!")
            
        except connector.Error as e:
            logging.error("[ERROR] Data insertion failed")
            raise ValueError(str(e))
    
    def __del__(self):
        logging.info("[INFO] Closing database connection")
        self.cursor.close()
        self.my_database.close()
