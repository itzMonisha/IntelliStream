from sqlalchemy import create_engine

DATABASE_URL = "postgresql://admin:admin123@postgres:5432/intellistream"

engine = create_engine(DATABASE_URL)
