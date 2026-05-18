import sqlite3

DATABASE_PATH = "crypto_prices.db"
SQL_FILE = "sql/create_tables.sql"

def create_database():
    """
    CREATE the SQLITE database and normalized crypto tables
    """
    conn = sqlite3.connect(DATABASE_PATH)

    with open(SQL_FILE, "r", encoding = "utf-8") as file:
        sql_script = file.read()

    conn.executescript(sql_script)

    conn.commit()
    conn.close()

    print("Database created succesfully")

if __name__ == "__main__":
    create_database()