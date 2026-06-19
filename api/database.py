from sqlalchemy import create_engine

DATABASE_URL = "postgresql://admin:admin123@127.0.0.1:5432/intellistream"

engine = create_engine(DATABASE_URL)
