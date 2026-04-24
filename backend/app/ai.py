# from sentence_transformers import SentenceTransformer
# from transformers import pipeline

# # 🔹 Embedding model
# embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# def get_embedding(text):
#     return embedding_model.encode(text).tolist()

# # 🔹 Summarization model (FREE 🔥)
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# def get_summary(text):
#     # limit input size (important)
#     text = text[:1000]

#     result = summarizer(text, max_length=150, min_length=50, do_sample=False)
    
#     return result[0]['summary_text']



# from transformers import pipeline
# import logging

# logging.basicConfig(level=logging.INFO)

# # ---------------- LOAD MODELS ----------------
# logging.info("Loading summarization model...")
# summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# logging.info("Loading feature extractor (for embeddings)...")
# embedder = pipeline("feature-extraction")

# # ---------------- EMBEDDINGS ----------------
# def get_embedding(text):
#     try:
#         result = embedder(text[:500])  # limit text
#         # simple flatten
#         embedding = [float(x) for x in result[0][0]]
#         return embedding
#     except Exception as e:
#         logging.error(f"Embedding failed: {str(e)}")
#         return []


# # ---------------- SUMMARY ----------------
# def get_summary(text):
#     try:
#         if not text.strip():
#             return "No content"

#         chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
#         summaries = []

#         for chunk in chunks[:2]:
#             result = summarizer(
#                 chunk,
#                 max_length=120,
#                 min_length=40,
#                 do_sample=False
#             )
#             summaries.append(result[0]['summary_text'])

#         return " ".join(summaries)

#     except Exception as e:
#         logging.error(f"Summary failed: {str(e)}")
#         return "Error"

import logging
import re
import hashlib

logging.basicConfig(level=logging.INFO)

# ---------------- EMBEDDING (Lightweight, no ML libs) ----------------
def get_embedding(text):
    """Generate embedding using lightweight hash-based method"""
    try:
        text = text or ""
        # Create a 512-dimensional embedding using hash values
        embedding = []
        words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
        
        # Build embedding by hashing words and mapping to 512 dimensions
        for i in range(512):
            hash_input = f"{' '.join(words)}-{i}"
            hash_obj = hashlib.md5(hash_input.encode())
            hash_value = int(hash_obj.hexdigest(), 16)
            # Normalize to [-1, 1] range
            value = (hash_value % 1000) / 500.0 - 1.0
            embedding.append(value)
        
        return embedding
    except Exception as e:
        logging.error(f"Embedding error: {e}")
        # Return zero vector on error
        return [0.0] * 512


# ---------------- SUMMARY ----------------
def get_summary(text):
    try:
        clean_text = text.strip()
        if not clean_text:
            return "No summary generated"

        # Keep the summarizer dependency-free so it works in lightweight envs.
        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+", clean_text)
            if sentence.strip()
        ]

        if not sentences:
            return clean_text[:300]

        word_pattern = re.compile(r"\b[a-zA-Z]{3,}\b")
        word_counts = {}
        for word in word_pattern.findall(clean_text.lower()):
            word_counts[word] = word_counts.get(word, 0) + 1

        ranked_sentences = []
        for index, sentence in enumerate(sentences):
            words = word_pattern.findall(sentence.lower())
            if not words:
                continue

            score = sum(word_counts.get(word, 0) for word in words) / len(words)
            ranked_sentences.append((score, index, sentence))

        if not ranked_sentences:
            return " ".join(sentences[:3])[:500]

        top_sentences = sorted(ranked_sentences, key=lambda item: item[0], reverse=True)[:3]
        ordered_summary = " ".join(
            sentence for _, _, sentence in sorted(top_sentences, key=lambda item: item[1])
        )

        return ordered_summary[:700] if ordered_summary else "No summary generated"

    except Exception as e:
        logging.error(f"Summary error: {e}")
        return "Error generating summary"
