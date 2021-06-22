import asyncio
import sqlite3

DB = '../proxy.db'
PROXY_TABLE = 'proxy_ip'


def create_proxy_table():
    conn = sqlite3.connect(DB, isolation_level=None)
    c = conn.cursor()
    c.execute(
        f"""
            CREATE TABLE IF NOT EXISTS {PROXY_TABLE} (
                idx INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                ip TEXT(15) NOT NULL,
                port INTEGER NOT NULL,
                CHECK (LENGTH(ip)<= 15),
                CHECK (LENGTH(port)<= 5),
                CONSTRAINT {PROXY_TABLE}_UN UNIQUE (ip,port)
            );
        """
    )
    conn.commit()
    conn.close()


def with_conn(func):
    def a(*args, **kwargs):
        conn = sqlite3.connect(DB)
        try:
            print(func.__name__)
            return func(conn, *args, **kwargs)
        finally:
            conn.close()

    return a


@with_conn
def select_all_proxy(conn):
    cur = conn.cursor()
    cur.execute(f'select ip, port from {PROXY_TABLE}')
    return cur.fetchall()


@with_conn
def migrate(conn):
    cur = conn.cursor()
    cur.execute(f'select ip, port from {PROXY_TABLE}')
    return cur.fetchall()


@with_conn
def insert_proxy_row(conn, *rows: tuple):
    all_proxy = select_all_proxy()

    inter = set(all_proxy).intersection(set(rows))
    add_proxy = tuple(set(rows) - set(all_proxy))
    print(f'add: {len(add_proxy)}, exist: {len(inter)}')

    conn.executemany(f'insert into {PROXY_TABLE}(ip, port) values(?, ?);', add_proxy)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # insert_proxy_row((1, 2), (3, 4))
    pass
