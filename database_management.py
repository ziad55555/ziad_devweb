"""Backend Model-First Database management with schema models."""
import sqlalchemy.dialects.mysql.pymysql
import sqlalchemy
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Sequence,
    ForeignKey,
    create_engine,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database


USER = "test2"
PASSWORD = "test2"
HOST = "localhost"
PORT = "5432"

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    username = Column(String(20), unique=True)
    firstName = Column(String(20))
    lastName = Column(String(20))
    email = Column(String(50), unique=True)
    avatar = Column(String(20))

    # Relation : un utilisateur peut avoir plusieurs posts
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

    # Relation : un utilisateur peut liker plusieurs posts
    stars = relationship("Star", back_populates="user", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, Sequence("post_id_seq"), primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created = Column(DateTime(), nullable=False)
    title = Column(String(200), nullable=False)
    body = Column(String(2000), nullable=False)

    # Relation : un post a un auteur
    author = relationship("User", back_populates="posts")

    # Relation : un post peut être liké par plusieurs utilisateurs
    stars = relationship("Star", back_populates="post", cascade="all, delete-orphan")


class Star(Base):
    __tablename__ = "stars"
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    # Relation : lien vers le post liké
    post = relationship("Post", back_populates="stars")

    # Relation : lien vers l'utilisateur qui a liké
    user = relationship("User", back_populates="stars")


class database_management:
    def __init__(self, db_name: str, recreate: bool):
        self.engine = create_engine(
            f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{db_name}"
        )
        self.db_name = db_name

        if recreate:
            if database_exists(self.engine.url):
                drop_database(self.engine.url)

        if not database_exists(self.engine.url):
            self.create_db()
        if not sqlalchemy.inspect(self.engine).has_table("users"):
            self.create_tables()

    def create_db(self):
        create_database(self.engine.url)

    def create_tables(self):
        Base.metadata.create_all(self.engine)
        with self.engine.connect() as conn:
            conn.execute(text("CREATE SEQUENCE IF NOT EXISTS post_id_seq"))
            conn.execute(text("CREATE SEQUENCE IF NOT EXISTS user_id_seq"))


if __name__ == "__main__":
    db = database_management("blog_database_test2", recreate=True)
    print("Base de données initialisée avec succès.")
