import os
import sqlite3
import struct
from typing import List

import sqlean
import sqlean.dbapi2
import sqlite_vec


def serialize_f32(vector: List[float]) -> bytes:
    """serializes a list of floats into a compact "raw bytes" format"""
    return struct.pack("%sf" % len(vector), *vector)


def connect() -> sqlite3.Connection:
    connection: sqlite3.Connection = sqlean.connect("totem.db")  # type: ignore
    connection.enable_load_extension(True)
    sqlite_vec.load(connection)
    connection.enable_load_extension(False)
    return connection


def delete_database():
    os.remove("totem.db")
