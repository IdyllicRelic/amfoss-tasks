from sqlite3 import connect

import discord

DB = "database.db"


def init_db():
    with connect(DB) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            balance INTEGER DEFAULT 0,
            last_daily TEXT,
            last_rob TEXT
            )""")

        con.commit()


def get_balance(user: discord.Member) -> int:
    with connect(DB) as con:
        cur = con.cursor()

        row = cur.execute(
            "SELECT balance FROM users WHERE user_id = ?", (user.id,)
        ).fetchone()

        if row is None:
            cur.execute(
                "INSERT OR IGNORE INTO users(user_id, username) VALUES(?, ?)",
                (user.id, user.name),
            )
            return 0

        return row[0]


def update_balance(user: discord.Member, balance: int):
    with connect(DB) as con:
        cur = con.cursor()

        cur.execute(
            "UPDATE users SET balance = ? WHERE user_id = ?", (balance, user.id)
        )

        con.commit()


def get_worst_generation() -> list[tuple[str, int]]:
    with connect(DB) as con:
        cur = con.cursor()

        cur.execute("SELECT username, balance FROM users ORDER BY balance DESC")

        return cur.fetchmany(5)


def get_last_daily(user: discord.Member) -> str:
    with connect(DB) as con:
        cur = con.cursor()
        cur.execute("SELECT last_daily FROM users WHERE user_id = ?", (user.id,))

        return cur.fetchone()[0]


def set_last_daily(user: discord.Member, date: str):
    with connect(DB) as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE users SET last_daily = ? WHERE user_id = ?", (date, user.id)
        )


def get_last_rob(user: discord.Member) -> str:
    with connect(DB) as con:
        cur = con.cursor()
        cur.execute("SELECT last_rob FROM users WHERE user_id = ?", (user.id,))

        return cur.fetchone()[0]


def set_last_rob(user: discord.Member, date: str):
    with connect(DB) as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET last_rob = ? WHERE user_id = ?", (date, user.id))
