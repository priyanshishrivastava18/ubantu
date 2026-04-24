# from sqlalchemy import create_engine, text

# DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/document_intelligence_db"

# engine = create_engine(DATABASE_URL)

# # function to insert data
# def insert_document(filename, filepath):
#     with engine.connect() as conn:
#         conn.execute(
#             text("""
#             INSERT INTO document_aints (filename, filepath, status)
#             VALUES (:filename, :filepath, :status)
#             """),
#             {
#                 "filename": filename,
#                 "filepath": filepath,
#                 "status": "uploaded"
#             }
#         )
#         conn.commit()

# def get_document_path(document_id):
#     with engine.connect() as conn:
#         result = conn.execute(
#             text("SELECT filepath FROM document_aints WHERE id=:id"),
#             {"id": document_id}
#         ).fetchone()
        
#         return result[0] if result else None   

# def insert_chunks(document_id, chunks):
#     with engine.connect() as conn:
#         for chunk in chunks:
#             conn.execute(
#                 text("""
#                 INSERT INTO document_chunks (document_id, chunk_text)
#                 VALUES (:doc_id, :chunk)
#                 """),
#                 {
#                     "doc_id": document_id,
#                     "chunk": chunk
#                 }
#             )
#         conn.commit() 
# def insert_summary(document_id, summary):
#     with engine.connect() as conn:
#         conn.execute(
#             text("""
#             INSERT INTO ai_summaries (document_id, summary)
#             VALUES (:doc_id, :summary)
#             """),
#             {
#                 "doc_id": document_id,
#                 "summary": summary
#             }
#         )
#         conn.commit()               


# from sqlalchemy import create_engine, text
# import os
# from dotenv import load_dotenv
# from pathlib import Path
# import logging

# # ---------------- SETUP LOGGING ----------------
# LOG_DIR = "/opt/app/logs/"
# os.makedirs(LOG_DIR, exist_ok=True)

# logging.basicConfig(
#     filename=os.path.join(LOG_DIR, "db.log"),
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# # ---------------- LOAD .env SAFELY ----------------
# env_path = Path(__file__).resolve().parent.parent.parent / ".env"
# load_dotenv(dotenv_path=env_path)

# DATABASE_URL = os.getenv("DATABASE_URL")

# print("DEBUG ENV PATH:", env_path)
# print("DEBUG DATABASE_URL:", DATABASE_URL)

# if not DATABASE_URL:
#     raise Exception("DATABASE_URL not loaded! Check .env file location or name")

# # ---------------- CREATE ENGINE ----------------
# engine = create_engine(
#     DATABASE_URL,
#     pool_size=5,
#     max_overflow=10
# )

# # ---------------- INSERT DOCUMENT ----------------
# def insert_document(filename, filepath):
#     try:
#         with engine.begin() as conn:
#             conn.execute(
#                 text("""
#                     INSERT INTO document_aints (filename, filepath, status)
#                     VALUES (:filename, :filepath, :status)
#                 """),
#                 {
#                     "filename": filename,
#                     "filepath": filepath,
#                     "status": "uploaded"
#                 }
#             )
#         logging.info(f"Inserted document: {filename}")
#     except Exception as e:
#         logging.error(f"Insert document failed: {str(e)}")
#         raise


# # ---------------- GET DOCUMENT PATH ----------------
# def get_document_path(document_id):
#     try:
#         with engine.connect() as conn:
#             result = conn.execute(
#                 text("SELECT filepath FROM document_aints WHERE id=:id"),
#                 {"id": document_id}
#             ).fetchone()

#             return result[0] if result else None
#     except Exception as e:
#         logging.error(f"Fetch document failed: {str(e)}")
#         return None


# # ---------------- INSERT CHUNKS + EMBEDDINGS ----------------
# def insert_chunks(document_id, chunks, embeddings):
#     try:
#         with engine.begin() as conn:
#             for chunk, emb in zip(chunks, embeddings):
#                 conn.execute(
#                     text("""
#                         INSERT INTO document_chunks (document_id, chunk_text, embedding)
#                         VALUES (:doc_id, :chunk, :embedding)
#                     """),
#                     {
#                         "doc_id": document_id,
#                         "chunk": chunk,
#                         "embedding": str(emb)  # temporary storage
#                     }
#                 )
#         logging.info(f"Inserted chunks for document ID: {document_id}")
#     except Exception as e:
#         logging.error(f"Insert chunks failed: {str(e)}")
#         raise


# # ---------------- INSERT SUMMARY ----------------
# def insert_summary(document_id, summary):
#     try:
#         with engine.begin() as conn:
#             conn.execute(
#                 text("""
#                     INSERT INTO ai_summaries (document_id, summary)
#                     VALUES (:doc_id, :summary)
#                 """),
#                 {
#                     "doc_id": document_id,
#                     "summary": summary
#                 }
#             )
#         logging.info(f"Inserted summary for document ID: {document_id}")
#     except Exception as e:
#         logging.error(f"Insert summary failed: {str(e)}")
#         raise

import os
from dotenv import load_dotenv
from pathlib import Path
import logging
import json
import math

# Try to use SQLAlchemy if available, otherwise use in-memory storage
try:
    from sqlalchemy import create_engine, text
    USE_DB = True
except:
    USE_DB = False

# ---------------- LOGGING SETUP ----------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "db.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ============ IN-MEMORY STORAGE (No DB Required) ============
documents = {}
chunks_data = {}
summaries_data = {}
doc_counter = 0

# ============ DATABASE FALLBACK ============
if USE_DB:
    try:
        env_path = Path(__file__).resolve().parent.parent.parent / ".env"
        load_dotenv(dotenv_path=env_path)
        DATABASE_URL = os.getenv("DATABASE_URL")
        engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10, pool_pre_ping=True)
    except:
        USE_DB = False
        logging.warning("Database connection failed, using in-memory storage")

# ============ INSERT DOCUMENT ============
def insert_document(filename, filepath):
    global doc_counter
    try:
        if USE_DB:
            with engine.begin() as conn:
                conn.execute(
                    text("""
                        INSERT INTO uploaded_documents (filename, filepath, status)
                        VALUES (:filename, :filepath, :status)
                    """),
                    {
                        "filename": filename,
                        "filepath": filepath,
                        "status": "uploaded"
                    }
                )
        else:
            doc_counter += 1
            documents[doc_counter] = {
                "id": doc_counter,
                "filename": filename,
                "filepath": filepath,
                "status": "uploaded"
            }
        
        logging.info(f"Inserted document: {filename}")
    except Exception as e:
        logging.error(f"Insert document failed: {str(e)}")
        if USE_DB:
            raise

# ============ GET DOCUMENT PATH ============
def get_document_path(document_id):
    try:
        if USE_DB:
            with engine.connect() as conn:
                result = conn.execute(
                    text("SELECT filepath FROM uploaded_documents WHERE id=:id"),
                    {"id": document_id}
                ).fetchone()
                return result[0] if result else None
        else:
            doc = documents.get(document_id)
            return doc["filepath"] if doc else None
    except Exception as e:
        logging.error(f"Fetch document failed: {str(e)}")
        return None

# ============ INSERT CHUNKS ============
def insert_chunks(document_id, chunks, embeddings):
    try:
        if USE_DB:
            with engine.begin() as conn:
                conn.execute(
                    text("DELETE FROM document_chunks WHERE document_id = :doc_id"),
                    {"doc_id": document_id}
                )
                for chunk, emb in zip(chunks, embeddings):
                    conn.execute(
                        text("""
                            INSERT INTO document_chunks (document_id, chunk_text, embedding)
                            VALUES (:doc_id, :chunk, :embedding)
                        """),
                        {
                            "doc_id": document_id,
                            "chunk": chunk,
                            "embedding": json.dumps(emb)
                        }
                    )
        else:
            chunks_data[document_id] = [
                {"text": chunk, "embedding": emb}
                for chunk, emb in zip(chunks, embeddings)
            ]
        
        logging.info(f"Inserted chunks for document ID: {document_id}")
    except Exception as e:
        logging.error(f"Insert chunks failed: {str(e)}")
        if USE_DB:
            raise

# ============ INSERT SUMMARY ============
def insert_summary(document_id, summary):
    try:
        if USE_DB:
            with engine.begin() as conn:
                conn.execute(
                    text("""
                        INSERT INTO ai_summaries (document_id, summary)
                        VALUES (:doc_id, :summary)
                    """),
                    {
                        "doc_id": document_id,
                        "summary": summary
                    }
                )
        else:
            summaries_data[document_id] = summary
        
        logging.info(f"Inserted summary for document ID: {document_id}")
    except Exception as e:
        logging.error(f"Insert summary failed: {str(e)}")
        if USE_DB:
            raise


# ---------------- COSINE SIMILARITY ----------------
def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    return dot / (mag_a * mag_b + 1e-9)


# ---------------- SEARCH SIMILAR CHUNKS ----------------
def search_similar_chunks(query_embedding, limit=5):
    try:
        if not query_embedding:
            return []

        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT chunk_text, embedding
                    FROM document_chunks
                """)
            ).fetchall()

        results = []

        for row in result:
            chunk_text = row[0]
            emb = json.loads(row[1])   # ✅ now works

            if not emb or len(emb) != len(query_embedding):
                continue

            score = cosine_similarity(query_embedding, emb)

            results.append({
                "text": chunk_text,
                "score": score
            })

        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:limit]

    except Exception as e:
        logging.error(f"Search failed: {str(e)}")
        return []


# ---------------- GET ALL DOCUMENTS ----------------
def get_all_documents():
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT id, filename, filepath, status FROM uploaded_documents")
            ).fetchall()

        documents = []
        for row in result:
            documents.append({
                "id": row[0],
                "filename": row[1],
                "filepath": row[2],
                "status": row[3]
            })

        return documents

    except Exception as e:
        logging.error(f"Get all documents failed: {str(e)}")
        return []
