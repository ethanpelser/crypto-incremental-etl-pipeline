import sqlite3

DATABASE_PATH = "crypto_prices.db"
VALIDATION_SQL_PATH = "sql/validation_checks.sql"

def run_validation_checks():
    """
    RUN  SQL validations checks against the database
    """

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    with open(VALIDATION_SQL_PATH, "r", encoding = "utf-8") as file:
        sql_script = file.read()

    queries = sql_script.split(";")

    print("=" * 60)
    print("RUNNING VALIDATION CHECKS")
    print("=" * 60)

    for query in queries:
        query = query.strip()

        if not query:
            continue

        cursor.execute(query)
        results = cursor.fetchall()

        print("\nQUERY:")
        print(query)

        if results:
            for row in results[:10]:
                print(row)

        else:
            print("No results returned")

    conn.close()

if __name__ == "__main__":
    run_validation_checks()


