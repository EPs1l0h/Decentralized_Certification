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
        did_document TEXT
    )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS key (
            username INTEGER PRIMARY KEY AUTOINCREMENT,
            kid INTEGER NOT NULL,
            DID TEXT NOT NULL,
            type_of_key TEXT NOT NULL,
            public_key_pem TEXT,
            private_key_pem TEXT
        )
        ''')

    cursor.execute(('''CREATE TABLE IF NOT EXISTS VC (
        VC TEXT PRIMARY KEY
        )'''))

    cursor.execute(('''CREATE TABLE IF NOT EXISTS AskedVP ( 
       username TEXT PRIMARY KEY,
       datetime TEXT NOT NULL,
       ip_address TEXT NOT NULL
       )'''))


    conn.commit()
    conn.close()


def init_sqlite():
    init_db()

init_sqlite()