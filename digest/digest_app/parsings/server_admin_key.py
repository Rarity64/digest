#!/usr/bin/env python3
from dotenv import load_dotenv
import os
import sys

load_dotenv()

server_admin_key = os.getenv("SERVER_ADMIN_KEY")
salt = os.getenv("SALT")

def check(key):
    if not server_admin_key:
        print("SERVER_ADMIN_KEY not set", file=sys.stderr)
        return False
    return server_admin_key == key

def get_salt():
    return salt

if __name__ == '__main__':
    if not server_admin_key:
        print("SERVER_ADMIN_KEY not set", file=sys.stderr)
    print(str(check(input("To check, enter your key: "))).lower())
