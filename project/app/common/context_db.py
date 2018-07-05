from common import db
from common.db import open_db, close_db


class DataConns():
    """上下文操作数据库"""
    def __init__(self):
        open_db()

    def __enter__(self):
        pass
    def __exit__(self, exc_t, exc_v, traceback):
        close_db()

if __name__ == "__main__":
    with DataConns() as Conn:
        db.insert('','','')
        pass



