import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="",
    port="",
    user="postgres",
    password=""
)

def save_message(role, content, status=None):

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO messages (role, content, status)
        VALUES (%s, %s, %s)
    """, (role, content, status))

    conn.commit()
    cur.close()

def get_history(limit=20):

    cur = conn.cursor()

    cur.execute("""
        SELECT role, content
        FROM messages
        ORDER BY id DESC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()

    cur.close()

    rows.reverse()

    return [
        {
            "role": role,
            "content": content,
        }
        for role, content in rows
    ]
    
def clear_history():

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM messages")
    print("Antes:", cur.fetchone())

    cur.execute("DELETE FROM messages")

    conn.commit()

    cur.execute("SELECT COUNT(*) FROM messages")
    print("Depois:", cur.fetchone())

    cur.close()
