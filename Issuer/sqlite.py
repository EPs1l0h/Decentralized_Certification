# -*- coding: utf-8 -*-
# 初始化数据库和表
import sqlite3


def init_db():
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Holder (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account TEXT NOT NULL,
        password TEXT NOT NULL,
        addr TEXT NOT NULL,
        private_key TEXT NOT NULL,
        did TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

init_db()