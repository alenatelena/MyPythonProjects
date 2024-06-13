from sqlalchemy import Column, Integer, String, and_, create_engine, exc, select
from contextlib import contextmanager
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

db_uri = 'sqlite:///./prompt.db'
engine = create_engine(
    db_uri, connect_args={"check_same_thread": False}
)

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String, unique=True)
    password: str = Column(String)
    name: str = Column(String)
    surname: str = Column(String)
    phone: str = Column(String)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# создаем таблицы
Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate(username: str, password: str):
    user = select(User).where(and_(User.username == username))
    with contextmanager(get_db)() as db:
        try:
            auth_user = db.execute(user)
        except:
            return False
        if auth_user.password == password:
            return True
        else:
            return False

def register(name: str, surname: str, username: str, password: str, phone: str):
    new_user = User(name=name, surname=surname, username=username, password=password, phone=phone)
    with contextmanager(get_db)() as db:
        try:
            db.add(new_user)
            db.commit()
        except exc.SQLAlchemyError as e:
            return 'Ошибка при заполнении данных'

