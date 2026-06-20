import psycopg2

try:
    print("Trying connection...")

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="intellistream",
        user="admin",
        password="admin123"
    )

    print("Connected Successfully")

    cur = conn.cursor()
    cur.execute("SELECT current_user;")
    print(cur.fetchone())

    conn.close()

except Exception as e:
    print("Error:", e)