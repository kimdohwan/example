import sqlite3
from os.path import join, dirname, abspath

DB_SQLITE = 'proxy.db'
# DB_SQLITE = 'proxy_test.db'
DB_SQLITE_PATH = join(dirname(dirname(dirname(abspath(__file__)))), DB_SQLITE)

TABLE_PROXY_IP = 'proxy_ip'
TABLE_PROXY_HISTORY = 'proxy_history'


def with_conn(func):
    def a(*args, **kwargs):
        conn = sqlite3.connect(DB_SQLITE_PATH)
        conn.cursor().execute(
            """
            PRAGMA foreign_keys = ON
            """
        )
        conn.commit()
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
    c.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_PROXY_HISTORY} (
        idx INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        proxy_ip_idx INTEGER NOT NULL,
        content TEXT(100) NOT NULL,
        url TEXT(100),
        CONSTRAINT {TABLE_PROXY_HISTORY}_FK FOREIGN KEY (proxy_ip_idx) REFERENCES {TABLE_PROXY_IP}(idx) ON DELETE CASCADE);
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


create_proxy_table()

# if __name__ == '__main__':
#     # insert_proxy_row((1, 2), (3, 4))
#     # create_proxy_table()
#     # a = select_all_proxy()
#     print(1)
