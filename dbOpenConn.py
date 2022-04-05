import mysql.connector as sql
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def openDBConnection():
    return sql.connect(
        user=getenv('NAME'),
        password=getenv('PASS'),
        host=getenv('HOST'),
        database=getenv('DB')
    )