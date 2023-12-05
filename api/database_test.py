import unittest
import psycopg2 as db
import configparser
from dotenv import load_dotenv
import os

# Define your database operations functions directly within the test class or use lambda functions
def insert_data(conn, curs, data):
    try:
        curs.execute("""INSERT INTO test VALUES (%s, %s, %s);""", (data['name'], data['age'], data['email']))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def get_data(curs, name):
    try:
        curs.execute("""SELECT * FROM test WHERE name = %s;""", (name,))
        result = curs.fetchone()
    except Exception as e:
        print(f"Error: {e}")
    return result

def update_data(conn, curs, data):
    try:
        curs.execute("""UPDATE test SET age = %s, email = %s WHERE name = %s;""",
                     (data['age'], data['email'], data['name']))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def clean_up(conn, curs, data):
    try:
        curs.execute("""DELETE FROM test WHERE name = %s;""",
                     (data['name'],))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

# Define a class for your database tests
class DatabaseTests(unittest.TestCase):

    # Set up a testing database connection before each test
    def setUp(self):
        # Use a separate testing database or create a temporary schema for testing
        config = configparser.ConfigParser()
        config.read('dbtool.ini')

        if os.getenv("VERCEL"):
            # Load environment variables from Vercel secrets
            password = os.environ.get('DATABASE_KEY')
        elif os.getenv("GIT_DATABASE"):
            password = os.environ.get('GIT_DATABASE')
        else:
            # Load environment variables from the .env file
            load_dotenv()
            password = os.environ.get("DATABASE")

        config['connection']['password'] = password

        self.conn = db.connect(**config['connection'])
        self.cursor = self.conn.cursor()


    # Tear down the testing database connection after each test
    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    # Test the insert_data function
    def test_insert_data(self):
        # Define your test data
        test_data = {"name": "John Doe", "age": 25, "email": "john.doe@example.com"}

        # Call the provided insert_data function
        insert_data(self.conn, self.cursor, test_data)

        # Query the database to check if the data was inserted
        self.cursor.execute("""SELECT * FROM test WHERE name = 'John Doe';""")
        result = self.cursor.fetchone()

        clean_up(self.conn, self.cursor, test_data)

        # Assert that the result matches the inserted data
        self.assertIsNotNone(result)
        self.assertEqual(result[0], test_data["name"])
        self.assertEqual(result[1], test_data["age"])
        self.assertEqual(result[2], test_data["email"])

    # Test the get_data function
    def test_get_data(self):
        # Insert test data into the database
        test_data = {"name": "Jane Doe", "age": 30, "email": "jane.doe@example.com"}
        insert_data(self.conn, self.cursor, test_data)

        # Call the provided get_data function
        result = get_data(self.cursor, "Jane Doe")

        clean_up(self.conn, self.cursor, test_data)

        # Assert that the result matches the expected data
        self.assertIsNotNone(result)
        self.assertEqual(result[0], test_data["name"])
        self.assertEqual(result[1], test_data["age"])
        self.assertEqual(result[2], test_data["email"])

    # Test the update_data function
    def test_update_data(self):
        # Insert test data into the database
        test_data = {"name": "Bob Smith", "age": 35, "email": "bob.smith@example.com"}
        insert_data(self.conn, self.cursor, test_data)

        # Update the test data
        updated_data = {"name": "Bob Smith", "age": 36, "email": "bob.smith.updated@example.com"}
        update_data(self.conn, self.cursor, updated_data)

        # Query the database to check if the data was updated
        self.cursor.execute("SELECT * FROM test WHERE name = 'Bob Smith'")
        result = self.cursor.fetchone()

        clean_up(self.conn, self.cursor, test_data)

        # Assert that the result matches the updated data
        self.assertIsNotNone(result)
        self.assertEqual(result[0], updated_data["name"])
        self.assertEqual(result[1], updated_data["age"])
        self.assertEqual(result[2], updated_data["email"])

if __name__ == '__main__':
    unittest.main()
