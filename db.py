import sqlalchemy
from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.automap import automap_base, name_for_collection_relationship, name_for_scalar_relationship

USER = "debweb_user_admin"
PASSWORD = "tutu"
HOST = "localhost"
PORT = "5432"
DB_NAME = "blog_database2"

TRACE = True # pour déboguer

# Les éléments suivants seront définis lorsque l'automap aura fait son
# travail...
User = None
Post = None
Star = None

class DBAccess:
    def __init__(self, db_name: str, recreate: bool):
        self.connect_db()

    def connect_db(self):
        '''Connextion à la base de données via l'automap'''

        # ORM: correpondances nom de table => nom de classe
        model_map = {
            'user': 'User',
            'post': 'Post',
            'star': 'Star',
        }

        # ORM: correpondances association => attribut
        relation_map = {
            # l'association 1:N entre User et Post
            'User=>Post(post_author_id_fkey)': 'all_posts',
            'Post=>User(post_author_id_fkey)': 'author',
            # l'association N:M entre Post et User (via Star)
            'Post=>Star(star_post_id_fkey)': 'all_stars',
            'User=>Star(star_user_id_fkey)': 'all_stars',
            'Post=>User(star_post_id_fkey)': 'all_starring_users',
            'User=>Post(star_user_id_fkey)': 'all_starred_posts',
        }

        url_de_connexion = (
            "postgresql+psycopg2://"
            + USER
            + ":" + PASSWORD
            + "@" + HOST
            + ":" + PORT
            + "/" + DB_NAME
        )

        if TRACE:
            print(f"Database URL: {url_de_connexion}")

        sqlalchemy_engine_echo = False # True pour déboguer

        self.engine = create_engine(
            url_de_connexion,
            # si True, pratique pour déboguer (mais très verbeux)
            echo=sqlalchemy_engine_echo,
            # pour disposer des fonctionnalités de la version 2.0
            future=True,
        )
        our_metadata = MetaData()
        our_metadata.reflect(self.engine, only=model_map.keys())
        # print("our_metadata: ok")
        Base = automap_base(metadata=our_metadata)

        class User(Base):
            __tablename__ = 'user'

            # la déclaration suivante est indispensable (pour le viewonly)
            all_starred_posts = relationship(
                "Post", collection_class=set, secondary="star", viewonly=True
            )

            def __str__(self):
                return f"User({self.id},{self.username})"

        class Post(Base):
            __tablename__ = 'post'

            # la déclaration suivante est indispensable (pour le viewonly)
            all_starring_users = relationship(
                "User", collection_class=set, secondary="star", viewonly=True
            )

            def __str__(self):
                return f"Post({self.id},{self.author_id},{self.created})"

        class Star(Base):
            __tablename__ = 'star'

            def __str__(self):
                return f"Star({self.user_id},{self.post_id})"

        def map_names(type, orig_func):
            """fonction d'aide à la mise en correspondance"""
            def _map_names(base, local_cls, referred_cls, constraint):
                auto_name = orig_func(base, local_cls, referred_cls, constraint)
                # la clé de l'association
                key = f"{local_cls.__name__}=>{referred_cls.__name__}({constraint.name})"
                # quelle correpondance ?
                if key in relation_map:
                    # Yes, return it
                    name = relation_map[key]
                else:
                    name = auto_name
                if TRACE:
                    # affiche la relation créée (pour comprendre ce qui se passe)
                    print(f" {type:>10s}: {key} {auto_name} => {name}")
                return name

            return _map_names

        Base.prepare(
            name_for_scalar_relationship=map_names('scalar', name_for_scalar_relationship),
            name_for_collection_relationship=map_names('collection', name_for_collection_relationship),
        )

        # On rend les tables du modèle globales à ce module
        for cls in [User, Post, Star]:
            cls.__table__.info = dict(bind_key='main')
            globals()[cls.__name__] = cls

        if TRACE:
            print("DB mapping done.")



# Base = declarative_base()


# class User(Base):
#     __tablename__ = "user"
#     id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
#     username = Column(Text, unique=True)
#     firstname = Column(Text)
#     lastname = Column(Text)
#     email = Column(Text, unique=True)
#     # avatar = Column(String(20))

# class Post(Base):
#     __tablename__ = "post"
#     id = Column(Integer, Sequence("post_id_seq"), primary_key=True)
#     author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
#     created = Column(DateTime(), nullable=False)
#     title = Column(Text, nullable=False)
#     body = Column(Text, nullable=False)


# class Star(Base):
#     __tablename__ = "star"
#     post_id = Column(Integer, ForeignKey("post.id"), nullable=False, primary_key=True)
#     user_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)



# class database_management:
#     def __init__(self, db_name: str, recreate: bool):
#         self.engine = create_engine(
#             f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{db_name}",
#             echo=True,
#         )
#         self.db_name = db_name

#         # if recreate:
#         #     if database_exists(self.engine.url):
#         #         drop_database(self.engine.url)

#         if not database_exists(self.engine.url):
#             self.create_db()
#         if not sqlalchemy.inspect(self.engine).has_table("user"):
#             self.create_tables()

#     def create_db(self):
#         create_database(self.engine.url)

#     def create_tables(self):
#         Base.metadata.create_all(self.engine)
