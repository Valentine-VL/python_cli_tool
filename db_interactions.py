import os
import sqlite3
from datetime import timedelta, datetime

from cryptography.fernet import Fernet


class DB:
    def __init__(self):
        self.conn = sqlite3.connect(os.getcwd() + '/test_db.db')
        self.cursor = self.conn.cursor()
        self.initial_tables_creation()
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def table_exists(self, table_name):
        result = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        return result.fetchone() is not None

    def initial_tables_creation(self):
        if not self.table_exists('passwords') or not self.table_exists('tasks'):
            table_creation_query = '''
            CREATE TABLE IF NOT EXISTS main.passwords (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `name` VARCHAR(100) UNIQUE NOT NULL,
                `username` VARCHAR(100),
                `hashed_password` VARCHAR(255) UNIQUE NOT NULL,
                `date_updated` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            '''
            self.cursor.execute(table_creation_query)
        if not self.table_exists('tasks'):
            table_creation_query = '''
            CREATE TABLE IF NOT EXISTS main.tasks (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `name` VARCHAR(100) UNIQUE NOT NULL,
                `description` VARCHAR(255),
                `completed` VARCHAR(3) DEFAULT 'NO' NOT NULL
                )
            '''
            self.cursor.execute(table_creation_query)
        self.conn.commit()

    # PASSWORDS db functionality
    def add_password(self, name, username, hashed_password):
        self.cursor.execute("INSERT INTO passwords (name, username, hashed_password) VALUES (?, ?, ?)",
                            (name, username, hashed_password))
        self.conn.commit()

    def get_password(self, name):
        self.cursor.execute("SELECT name, username, hashed_password, date_updated FROM passwords WHERE name=?", (name,))
        row = list(self.cursor.fetchone())
        day_to_expiration = calculate_days_before_expiration(row[-1])
        row[-1] = f"{day_to_expiration} day(s)"
        return dict(zip(["name", "username", "password", "expires in"], row))

    def list_passwords(self):
        self.cursor.execute("SELECT name, username, date_updated FROM passwords")
        rows = self.cursor.fetchall()
        entries = [{"name": row[0], "username": row[1], "expires in": f"{calculate_days_before_expiration(row[2])} day(s)"} for row in rows]
        return entries

    def update_password(self, name, username, hashed_password):
        if username:
            self.cursor.execute("UPDATE passwords SET username=?, hashed_password=?, date_updated=CURRENT_TIMESTAMP WHERE name=?",
                                (username, hashed_password, name))
        else:
            self.cursor.execute("UPDATE passwords SET hashed_password=?, date_updated=CURRENT_TIMESTAMP WHERE name=?",
                                (hashed_password, name))
        self.conn.commit()

    def delete_password(self, name):
        self.cursor.execute("DELETE FROM passwords WHERE name=?", (name,))
        self.conn.commit()


    # TASKS db functionality
    def add_task(self, name, description):
        self.cursor.execute("INSERT INTO tasks (name, description) VALUES (?, ?)",
                            (name, description))
        self.conn.commit()

    def get_task(self, name):
        self.cursor.execute("SELECT name, description, completed FROM tasks WHERE name=?", (name,))
        row = self.cursor.fetchone()
        return dict(zip(["name", "description", "completed"], row))

    def list_tasks(self):
        self.cursor.execute("SELECT name, description, completed FROM tasks")
        rows = self.cursor.fetchall()
        entries = [dict(zip(["name", "description", "completed"], row)) for row in rows]
        return entries

    def complete_task(self, name, completed):
        self.cursor.execute(
            "UPDATE tasks SET completed=? WHERE name=?",
            (completed, name))
        self.conn.commit()

    def remove_task(self, name):
        self.cursor.execute("DELETE FROM tasks WHERE name=?", (name,))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()


def calculate_days_before_expiration(last_updated_time, expiration_period_days=5):
    date_format = '%Y-%m-%d %H:%M:%S'
    expiration_time = datetime.strptime(last_updated_time, date_format) + timedelta(days=expiration_period_days)
    current_time = datetime.now()

    if current_time > expiration_time:
        return "expired"

    days_remaining = (expiration_time - current_time).days
    return days_remaining