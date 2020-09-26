import os
from typing import Iterator
from contextlib import contextmanager

import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return

    pg_user = os.environ.get("PG_USER")
    pg_pass = os.environ.get("PG_PASS")
    pg_host = os.environ.get("PG_HOST")
    db_name = os.environ.get("DB_NAME")

    conn_str = f"postgres://{pg_user}:{pg_pass}@{pg_host}/{db_name}"

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)
    return SqlAlchemyBase


@contextmanager
def create_session() -> Iterator[Session]:
    global __factory
    session = None

    try:
        session = __factory()
        yield session
    except Exception:
        if session:
            session.rollback()
        raise
    else:
        session.commit()
    finally:
        if session:
            session.close()
