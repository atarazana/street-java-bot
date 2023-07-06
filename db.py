import sqlite3


def init_db():
    conn = sqlite3.connect("chatbot.db")

    c = conn.cursor()

    # Create table
    c.execute(
        """CREATE TABLE IF NOT EXISTS users
                 (user text PRIMARY KEY, namespace text, app text)"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS polls
                 (poll_name text PRIMARY KEY, status text, option_1 text,
                  option_1_count number, option_2 text, option_2_count number, option_3 text, option_3_count number)"""
    )

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


def open_poll(poll_name: str, option_1: str, option_2: str, option_3: str):
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    # This is open to SQL injection to some degree, should be
    c.execute(
        """INSERT
           INTO polls
           (poll_name, status, option_1, option_1_count, option_2, option_2_count, option_3, option_3_count)
           VALUES
           (:poll_name, :status, :option_1, :option_1_count, :option_2, :option_2_count, :option_3, :option_3_count)""",
        {
            "poll_name": poll_name,
            "status": "OPEN",
            "option_1": option_1,
            "option_1_count": 0,
            "option_2": option_2,
            "option_2_count": 0,
            "option_3": option_3,
            "option_3_count": 0,
        },
    )
    conn.commit()
    conn.close()


def close_poll(poll_name: str):
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    # This is open to SQL injection to some degree, should be
    c.execute("UPDATE polls SET status=:status WHERE poll_name=:poll_name", {"status": "CLOSED", "poll_name": poll_name})
    conn.commit()
    conn.close()


def reopen_poll(poll_name: str):
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    # This is open to SQL injection to some degree, should be
    c.execute("UPDATE polls SET status=:status WHERE poll_name=:poll_name", {"status": "OPEN", "poll_name": poll_name})
    conn.commit()
    conn.close()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_poll(poll_name: str):
    conn = sqlite3.connect("chatbot.db")
    conn.row_factory = dict_factory
    c = conn.cursor()
    # This is open to SQL injection to some degree, should be
    c.execute(
        """SELECT poll_name, status, option_1, option_1_count, option_2, option_2_count, option_3, option_3_count
           FROM polls WHERE poll_name=:poll_name""",
        {"poll_name": poll_name},
    )

    poll = c.fetchone()
    print(f"poll = {poll}")

    conn.commit()
    conn.close()

    return poll


def add_vote_to_poll(poll_name: str, option: str):
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    # This is open to SQL injection to some degree, should be
    c.execute(f"UPDATE polls SET {option}_count={option}_count+1 WHERE poll_name=:poll_name", {"poll_name": poll_name})
    conn.commit()
    conn.close()


def update_app(app, namespace, user):
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    # This is open to SQL injection to some degree, should be
    c.execute(
        "REPLACE INTO users(user, namespace, app) VALUES (:user,  :namespace, :app)",
        {
            "user": user,
            "app": app,
            "namespace": namespace,
        },
    )
    conn.commit()
    conn.close()


def select_app(user: str):
    conn = sqlite3.connect("chatbot.db")

    c = conn.cursor()
    # This is open to SQL injection to some degree, should be
    c.execute("SELECT app, namespace FROM users WHERE user = (:user)", {"user": user})
    result = c.fetchone()
    if result is not None:
        app = result[0]
        namespace = result[1]
        conn.close()
        return app, namespace
    return None
