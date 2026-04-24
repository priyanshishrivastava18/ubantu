# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Backend is running successfully 🚀"}
# from fastapi import FastAPI, UploadFile, File
# import os
# from PyPDF2 import PdfReader

# app = FastAPI()

# UPLOAD_FOLDER = "uploads"

# # Home API (check server working)
# @app.get("/")
# def home():
#     return {"message": "Server is running"}

# # Upload API
# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
    
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)

#     with open(file_path, "wb") as f:
#         f.write(await file.read())

#     return {"message": "File uploaded successfully", "filename": file.filename}

# # Extract text API
# @app.get("/extract/{filename}")
# def extract_text(filename: str):

#     file_path = os.path.join(UPLOAD_FOLDER, filename)

#     reader = PdfReader(file_path)

#     text = ""
#     for page in reader.pages:
#         if page.extract_text():
#             text += page.extract_text()

#     return {"text": text[:1000]}  # first 1000 chars

# from fastapi import FastAPI, UploadFile, File
# import os
# from PyPDF2 import PdfReader
# from db import insert_document   # 🔥 important

# app = FastAPI()

# UPLOAD_FOLDER = "uploads"

# # ensure uploads folder exists
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Home API
# @app.get("/")
# def home():
#     return {"message": "Server is running"}

# # Upload API (DB integrated)
# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
    
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)

#     try:
#         # save file
#         with open(file_path, "wb") as f:
#             f.write(await file.read())

#         # 🔥 save to database
#         insert_document(file.filename, file_path)

#         return {
#             "message": "File uploaded + saved in DB",
#             "filename": file.filename
#         }

#     except Exception as e:
#         return {"error": str(e)}

# # Extract text API
# @app.get("/extract/{filename}")
# def extract_text(filename: str):

#     file_path = os.path.join(UPLOAD_FOLDER, filename)

#     if not os.path.exists(file_path):
#         return {"error": "File not found"}

#     try:
#         reader = PdfReader(file_path)

#         text = ""
#         for page in reader.pages:
#             content = page.extract_text()
#             if content:
#                 text += content

#         if text.strip() == "":
#             return {"error": "No readable text"}

#         return {"text": text[:1000]}

#     except Exception as e:
#         return {"error": str(e)}


# from fastapi import FastAPI, UploadFile, File
# import os
# import logging
# from PyPDF2 import PdfReader
# from dotenv import load_dotenv

# # ---------------- LOAD ENV ----------------
# load_dotenv()

# # ---------------- LOGGING SETUP ----------------
# LOG_DIR = "/opt/app/logs/"
# UPLOAD_FOLDER = "/opt/app/uploads/"

# os.makedirs(LOG_DIR, exist_ok=True)
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# logging.basicConfig(
#     filename=os.path.join(LOG_DIR, "app.log"),
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# # ---------------- IMPORTS ----------------
# from .db import (
#     insert_document,
#     get_document_path,
#     insert_chunks,
#     insert_summary
# )

# from .ai import get_summary, get_embedding

# # ---------------- APP ----------------
# app = FastAPI()


# # ---------------- HOME ----------------
# @app.get("/")
# def home():
#     return {"message": "Server is running"}


# # ---------------- UPLOAD ----------------
# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)

#     try:
#         with open(file_path, "wb") as f:
#             f.write(await file.read())

#         insert_document(file.filename, file_path)

#         logging.info(f"File uploaded: {file.filename}")

#         return {
#             "message": "File uploaded + saved in DB",
#             "filename": file.filename
#         }

#     except Exception as e:
#         logging.error(f"Upload failed: {str(e)}")
#         return {"error": str(e)}


# # ---------------- EXTRACT ----------------
# @app.get("/extract/{filename}")
# def extract_text(filename: str):

#     file_path = os.path.join(UPLOAD_FOLDER, filename)

#     if not os.path.exists(file_path):
#         return {"error": "File not found"}

#     try:
#         reader = PdfReader(file_path)

#         text = ""
#         for page in reader.pages:
#             text += page.extract_text() or ""

#         logging.info(f"Text extracted from: {filename}")

#         return {"text": text[:1000]}

#     except Exception as e:
#         logging.error(f"Extraction failed: {str(e)}")
#         return {"error": str(e)}


# # ---------------- CHUNKING ----------------
# def chunk_text(text, size=300):
#     return [text[i:i+size] for i in range(0, len(text), size)]


# # ---------------- PROCESS (EMBEDDINGS) ----------------
# @app.post("/process/{document_id}")
# def process_document(document_id: int):

#     file_path = get_document_path(document_id)

#     if not file_path:
#         return {"error": "Document not found"}

#     try:
#         reader = PdfReader(file_path)

#         text = ""
#         for page in reader.pages:
#             text += page.extract_text() or ""

#         chunks = chunk_text(text)

#         embeddings = [get_embedding(chunk) for chunk in chunks]

#         insert_chunks(document_id, chunks, embeddings)

#         logging.info(f"Processed document ID: {document_id}")

#         return {
#             "message": "Processing complete",
#             "total_chunks": len(chunks)
#         }

#     except Exception as e:
#         logging.error(f"Processing failed: {str(e)}")
#         return {"error": str(e)}


# # ---------------- SUMMARY ----------------
# @app.post("/summary/{document_id}")
# def generate_summary(document_id: int):

#     file_path = get_document_path(document_id)

#     if not file_path:
#         return {"error": "Document not found"}

#     try:
#         reader = PdfReader(file_path)

#         text = ""
#         for page in reader.pages:
#             text += page.extract_text() or ""

#         summary = get_summary(text)

#         insert_summary(document_id, summary)

#         logging.info(f"Summary generated for document ID: {document_id}")

#         return {"summary": summary}

#     except Exception as e:
#         logging.error(f"Summary failed: {str(e)}")
#         return {"error": str(e)}

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel 
import os
import logging
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- PATH SETUP ----------------
# LOG_DIR = "/opt/app/logs/"
# UPLOAD_FOLDER = "/opt/app/uploads/"
LOG_DIR = "logs"
UPLOAD_FOLDER = "uploads"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- LOGGING ----------------
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------- IMPORTS ----------------
from .db import (
    insert_document,
    get_document_path,
    insert_chunks,
    insert_summary,
    search_similar_chunks 
)

from .ai import get_summary, get_embedding

# ---------------- APP ----------------

class QueryRequest(BaseModel):
    query: str


# ---------------- HELPER FUNCTION ----------------
def extract_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "Server is running"}


# ---------------- UPLOAD ----------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    safe_name = secure_filename(file.filename)
    if not safe_name:
        raise HTTPException(status_code=400, detail="Invalid filename")

    file_path = os.path.join(UPLOAD_FOLDER, safe_name)

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())

        insert_document(safe_name, file_path)

        logging.info(f"File uploaded: {safe_name}")

        return {
            "message": "File uploaded + saved in DB",
            "filename": safe_name
        }

    except Exception as e:
        logging.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- EXTRACT ----------------
@app.get("/extract/{filename}")
def extract_text(filename: str):

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        text = extract_pdf_text(file_path)

        logging.info(f"Text extracted from: {filename}")

        return {"text": text[:1000]}

    except Exception as e:
        logging.error(f"Extraction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- CHUNKING ----------------
def chunk_text(text, size=300):
    return [text[i:i + size] for i in range(0, len(text), size)]


# ---------------- PROCESS (EMBEDDINGS) ----------------
@app.post("/process/{document_id}")
def process_document(document_id: int):
    try:
        file_path = get_document_path(document_id)
        if not file_path:
            raise HTTPException(status_code=404, detail="Document not found")

        text = extract_pdf_text(file_path)

        chunks = chunk_text(text)
        if not chunks:
            raise HTTPException(status_code=400, detail="No text available to process")

        embeddings = [get_embedding(chunk) for chunk in chunks]

        insert_chunks(document_id, chunks, embeddings)

        logging.info(f"Processed document ID: {document_id}")

        return {
            "message": "Processing complete",
            "total_chunks": len(chunks)
        }

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- SUMMARY ----------------
@app.post("/summary/{document_id}")
def generate_summary(document_id: int):
    try:
        file_path = get_document_path(document_id)
        if not file_path:
            raise HTTPException(status_code=404, detail="Document not found")

        text = extract_pdf_text(file_path)
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text available to summarize")

        summary = get_summary(text)

        insert_summary(document_id, summary)

        logging.info(f"Summary generated for document ID: {document_id}")

        return {"summary": summary}

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Summary failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- SEARCH ----------------
@app.post("/search")
def semantic_search(request: QueryRequest):
    if not request.query.strip():
       raise HTTPException(status_code=400, detail="Query is required")

    query_embedding = get_embedding(request.query)
 
    results = search_similar_chunks(query_embedding)

    return {"results": results}


# ---------------- ASK ----------------
@app.post("/ask")
def ask_question(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query is required")

    query_embedding = get_embedding(request.query)
    chunks = search_similar_chunks(query_embedding)
    if not chunks:
        raise HTTPException(status_code=404, detail="No relevant chunks found")

    context = " ".join([c["text"] for c in chunks])

    answer = get_summary(context + "\n\nQuestion: " + request.query)

    return {"answer": answer}


# ---------------- DOCUMENTS ----------------
@app.get("/documents")
def get_documents():
    try:
        from .db import get_all_documents
        docs = get_all_documents()
        return docs
    except Exception as e:
        logging.error(f"Failed to get documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- DASHBOARD ----------------
@app.get("/dashboard")
def get_dashboard():
    try:
        from .db import get_all_documents
        docs = get_all_documents()
        total_documents = len(docs) if docs else 0
        total_queries = 0  # You can implement this based on your DB schema
        
        return {
            "total_documents": total_documents,
            "total_queries": total_queries
        }
    except Exception as e:
        logging.error(f"Failed to get dashboard data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
