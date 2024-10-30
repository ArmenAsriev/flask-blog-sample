import sqlite3
import time


class DataBase:
    def __init__(self, db):
        # Initialize the database object
        self.__db = db  # Store the database connection
        self.__cur = db.cursor()  # Create a cursor for executing SQL queries

    def get_objects(self, table):
        # Retrieve all objects from the specified table
        sql = f'SELECT * FROM {table}'  # SQL query to select all records from the table
        try:
            self.__cur.execute(sql)  # Execute the SQL query
            res = self.__cur.fetchall()  # Fetch all results from the query
            if res:
                return res  # Return the result if it's not empty
        except IOError:
            print('Error reading the database')  # Handle database read errors
        return []  # Return an empty list if there's an error or the result is empty

    def add_post(self, title, text):
        # Add a new post to the database
        try:
            tm = int(time.time())  # Get the current time as a UNIX timestamp

            # SQL query to add a record to the database
            sql = 'INSERT INTO posts VALUES(NULL, ?, ?, ?)'
            self.__cur.execute(sql, (title, text, tm))  # Execute the SQL query with parameters
            self.__db.commit()  # Save changes to the database
        except sqlite3.Error as e:
            print('Error adding the post to the database: ' + str(e))  # Handle addition errors
            return False  # Return False in case of an error
        return True  # Return True if the addition was successful

    def get_post(self, post_id):
        # Retrieve a post by its ID
        try:
            # Search for the post by id
            self.__cur.execute('SELECT title, text FROM posts WHERE id = ?', (post_id,))
            res = self.__cur.fetchone()  # Fetch one record from the result
            if res:
                return res  # Return the found post
        except sqlite3.Error as e:
            print('Error retrieving the post from the database:', str(e))  # Handle post retrieval errors
        return None, None  # Return None in case of an error or if the post does not exist

    def add_user(self, email, password):
        # Add a new user to the database
        try:
            tm = int(time.time())  # Get the current time as a UNIX timestamp
            sql = 'INSERT INTO users (email, password, created_at) VALUES (?, ?, ?)'  # SQL query to add a user
            self.__cur.execute(sql, (email, password, tm))  # Execute the SQL query with parameters
            self.__db.commit()  # Save changes to the database
            return True  # Return True if the addition was successful
        except sqlite3.IntegrityError:
            print('Error: a user with this email already exists.')  # Handle unique email errors
            return False  # Return False in case of an error
        except sqlite3.Error as e:
            print('Error adding the user to the database:', str(e))  # Handle other addition errors
            return False  # Return False in case of an error

    def get_user_by_email(self, email):
        # Retrieve a user by email
        try:
            sql = 'SELECT * FROM users WHERE email = ?'  # SQL query to find a user by email
            self.__cur.execute(sql, (email,))  # Execute the SQL query with parameters
            return self.__cur.fetchone()  # Return the found user
        except sqlite3.Error as e:
            print('Error retrieving the user from the database:', str(e))  # Handle user retrieval errors
            return None  # Return None in case of an error
