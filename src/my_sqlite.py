import sqlite3
from os.path import join, dirname, abspath

DB_SQLITE = 'proxy.db'
DB_SQLITE_PATH = join(dirname(dirname(abspath(__file__))), DB_SQLITE)

TABLE_PROXY_IP = 'proxy_ip'


def with_conn(func):
    def a(*args, **kwargs):
        conn = sqlite3.connect(DB_SQLITE_PATH)
        try:
            print(func.__name__)
            return func(conn, *args, **kwargs)
        finally:
            conn.close()

    return a


@with_conn
def create_proxy_table(conn):
    c = conn.cursor()
    c.execute(
        f"""
            CREATE TABLE IF NOT EXISTS {TABLE_PROXY_IP} (
                idx INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                ip TEXT(15) NOT NULL,
                port INTEGER NOT NULL,
                CHECK (LENGTH(ip)<= 15),
                CHECK (LENGTH(port)<= 5),
                CONSTRAINT {TABLE_PROXY_IP}_UN UNIQUE (ip,port)
            );
        """
    )
    conn.commit()


@with_conn
def select_all_proxy(conn):
    cur = conn.cursor()
    cur.execute(f'select ip, port from {TABLE_PROXY_IP}')
    return cur.fetchall()


@with_conn
def migrate(conn):
    cur = conn.cursor()
    cur.execute(f'select ip, port from {TABLE_PROXY_IP}')
    return cur.fetchall()


@with_conn
def bulk_insert_proxy(conn, *rows: tuple):
    all_proxy = select_all_proxy()

    inter = set(all_proxy).intersection(set(rows))
    add_proxy = tuple(set(rows) - set(all_proxy))
    print(f'add: {len(add_proxy)}, exist: {len(inter)}')

    conn.executemany(f'insert into {TABLE_PROXY_IP}(ip, port) values(?, ?);', add_proxy)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # insert_proxy_row((1, 2), (3, 4))
    pass
