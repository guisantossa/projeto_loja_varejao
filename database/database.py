from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
# Carregar variáveis de ambiente do .env
load_dotenv()

# URL de Conexão com o banco de dados
POSTGRES_DATA_BASE_URL = os.getenv("DB_URL")

engine = create_engine(POSTGRES_DATA_BASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()