import mysql.connector
from mysql.connector import Error


class IDatabaseConnection:
    """Interface for database connection."""

    def connect(self):
        raise NotImplementedError

    def get_cursor(self):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class DatabaseConnection(IDatabaseConnection):
    """Concrete implementation for MySQL database connection."""

    def __init__(self):
        self.mydb = None
        self.mycursor = None

    def connect(self):
        """Establish the database connection and create a cursor."""
        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  
                database="sampathdb",
                port=3306
            )
            self.mycursor = self.mydb.cursor(buffered=True)  
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def get_cursor(self):
        """Return the cursor for executing queries."""
        if self.mycursor is None:
            raise Exception("Database cursor is not initialized. Call connect() first.")
        return self.mycursor

    def commit(self):
        """Commit current transaction."""
        if self.mydb:
            self.mydb.commit()

    def close(self):
        """Close the cursor and the connection."""
        if self.mycursor:
            self.mycursor.close()
        if self.mydb:
            self.mydb.close()


class IAuthenticationService:
    """Interface for authentication service."""

    def authenticate(self, username, password):
        raise NotImplementedError


class AuthenticationService(IAuthenticationService):
    """Concrete implementation of authentication service."""

    def __init__(self, db_connection: IDatabaseConnection):
        self.db_connection = db_connection

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials against the database."""
        cursor = self.db_connection.get_cursor()
        query = "SELECT COUNT(*) FROM user WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        return result[0] == 1


# Example of usage in your system (like in BranchManager or ProductManager)
# db = DatabaseConnection()
# db.connect()
# auth_service = AuthenticationService(db)
# if auth_service.authenticate("admin", "adminpass"):
#     print("Authentication successful")
# else:
#     print("Authentication failed")
# db.close()
