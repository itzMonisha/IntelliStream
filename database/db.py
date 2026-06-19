from sqlalchemy import create_engine

DATABASE_URL = "postgresql://admin:admin123@localhost:5432/intellistream"

engine = create_engine(DATABASE_URL)
