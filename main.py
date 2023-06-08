import mariadb as db;
import sys;
import os;
from dotenv import load_dotenv




def main():
    
    print("Hello World!")
    
    try:
        conn = db.connect(
            user="root",
            password=os.environ.get('PASSWORD'),
            host="localhost",
            database="scott")
    except db.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
        
    cur = conn.cursor()
    print("SUCCESS: Connected to MariaDB Platform")
    print()
    
if __name__ == "__main__":
    load_dotenv()
    main()