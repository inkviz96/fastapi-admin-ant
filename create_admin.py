import bcrypt
from models import models
from sqlalchemy.orm import Session
from fastapi import Depends
from database.database_connection import get_db, engine, session

from utils.check_password import password_check
from distutils.util import strtobool

import sys

models.Base.metadata.create_all(bind=engine)


def create_user(username: str, password: str, db: Session = session):
    password = password
    bytePwd = password.encode('utf-8')

    # Generate salt
    mySalt = bcrypt.gensalt(16)

    # Hash password
    hash = bcrypt.hashpw(bytePwd, mySalt).decode()
    db_user = models.User(name=username, password=hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


if __name__ == '__main__':
    create = True
    user_name = input("Enter user name: ")
    password = input("Enter user password: ")
    password_repeat = input("Enter password again: ")
    if password != password_repeat:
        sys.stdout.write("Passwords not same")
        sys.exit(1)
    else:
        warnings = password_check(password)
        if warnings:
            for warn in warnings:
                sys.stdout.write(warn)
            create = strtobool(input("Create user(y/n): "))
        if create:
            create_user(username=user_name, password=password)
            sys.stdout.write(f"User {user_name} created")
            sys.exit(0)
        else:
            sys.exit(0)
