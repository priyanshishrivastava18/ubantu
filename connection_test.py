from sqlalchemy import create_engine
database_url = "postgresql://postgres:postgres123@127.0.0.1:5432/document_ai"
try:
   engine = create_engine(database_url)
   print(f"COnnection succesful {engine}")
except Exception as e:
    print(f"Database connection error: {e}")