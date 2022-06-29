import sqlite3
import psycopg2 as sql

database = sql.connect(
    database="d9obgpf4oco5p7",
    host="ec2-63-34-180-86.eu-west-1.compute.amazonaws.com",
    user="yzukespxjbwxlm",
    password="28825b18db0093fd31a285199ceda887ae67e80b923658e19100e9d82cbbadff"
)


# database = sqlite3.connect('bot.db')

cursor = database.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS translate(
    id INTEGER PRIMARY KEY,
    telegram_id TEXT,
    src TEXT,
    dest TEXT,
    original_text TEXT,
    translated_text TEXT
);
''')

database.commit()
database.close()
