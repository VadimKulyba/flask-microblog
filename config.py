import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        os.getenv("POSTGRES_USER", "microblog"),
        os.getenv("POSTGRES_PASSWORD", "microblog"),
        os.getenv("POSTGRES_HOST", "localhost"),
        os.getenv("POSTGRES_PORT", "5432"),
        os.getenv("POSTGRES_PDB", "microblog"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
