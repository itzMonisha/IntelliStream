import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv(
    "postgresql://intellistream_1_postgress_user:dg8iIlWtkRRrAUWN8O2NLz2ThVarmZW6@dpg-d8rbfomgvqtc73ertcv0-a.virginia-postgres.render.com/intellistream_1_postgress")

engine = create_engine(DATABASE_URL)
