import os
import sqlite3
import datetime

class SqliteLog:
    def __init__(self) -> None:
        self.conn = None
        self.cursor = None

    def _connect(self) -> None:
        if not os.path.exists('data'):
            os.makedirs('data')
        self.conn = sqlite3.connect('data/server.db')
        self.cursor = self.conn.cursor()

    def _create_table(self, table_name: str) -> None:
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                activity TEXT,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def _close(self) -> None:
        if self.conn:
            self.conn.close()

    def activity(self, ip: str, activity: str) -> str:
        try:
            self._connect()
            ip = ip.replace('.', '_')
            self._create_table(f'IP_{ip}')
            timestamp = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
            self.cursor.execute(f'''
                INSERT INTO IP_{ip} (activity, timestamp) VALUES (?, ?)
            ''', (activity, timestamp))
            self.conn.commit()
        except Exception as e:
           return e
        finally:
            self._close()
