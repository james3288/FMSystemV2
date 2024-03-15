import pyodbc

driver = "{ODBC Driver 17 for SQL Server}"
server = '192.168.2.96'
database = 'supply_db'
username = 'sa'
password = 'P@ssw0rd1!'

class SQLcon:
    def __init__(self):
        self.driver = driver
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.conn     = None 

    def connection(self):
        self.conn = pyodbc.connect('DRIVER='+ self.driver + ';SERVER='+ self.server +';DATABASE='+ self.database +';UID='+ self.username +';PWD='+ self.password)
        # self.conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;')
        cursor = self.conn.cursor()
        return cursor
    
    def connection2(self):
        conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        return conn

    def has_connection(self)-> False:
        try:
            # Establish a connection to the database
            self.conn = pyodbc.connect(
                f'DRIVER={self.driver};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                f'UID={self.username};'
                f'PWD={self.password};'
                #f'Trusted_Connection=False;'
                f'Connection Timeout=30;'
            )

            # Print a success message if the connection is established
            self.msg = "Connection established successfully"
            print(self.msg)
            # Close the connection
            self.conn.close()
            return True
            

        except pyodbc.Error as e:
            # Print an error message if the connection fails
            self.msg = f"Connection failed, error message: {e}"
            print(self.msg)
            return False
        


