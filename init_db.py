from sqlalchemy import create_engine


def db_start():
    engine = create_engine('sqlite:///tmp/test/db', convert_unicode=True)
