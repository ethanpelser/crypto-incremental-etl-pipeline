import sqlite3

DATABASE_PATH = "crypto_prices.db"
SQL_ANALYTICS = "sql/analytical_queries.sql"

def run_analytics():
    """
    Runs anylytical queries against crypto_pirces database
    """

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    with open(SQL_ANALYTICS, "r", encoding = "utf-8") as file:
        sql_queries = file.read()

    queries = sql_queries.split(";")
    
    print("=" *50)
    print('Runnin anlytical queries')
    print("=" *50)
    
    for query in queries:
        query = query.strip()
        print(query)

        if not query:
            continue

        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            for row in results:
                print(row[:10])

        else:
            print("No results returned")
    conn.close()

if __name__ == "__main__":
    run_analytics()


