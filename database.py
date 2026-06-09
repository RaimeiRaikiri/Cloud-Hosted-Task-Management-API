from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

db_password = os.getenv("postgres_password")

db_url = f"postgresql://postgres:{db_password}@localhost:5432/taskdb"

engine = create_engine(db_url)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)